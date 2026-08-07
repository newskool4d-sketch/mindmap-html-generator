#!/usr/bin/env node
import { existsSync, mkdirSync, readdirSync, writeFileSync } from "node:fs";
import { basename, dirname, extname, join, resolve } from "node:path";
import { pathToFileURL } from "node:url";
import { chromium } from "playwright";

const DEFAULT_EVIDENCE_DIR = ".omo/evidence/design-next";
const DEFAULT_OUT_DIR = `${DEFAULT_EVIDENCE_DIR}/screenshots`;
const DEFAULT_VIEWPORTS = "1280,768,390";
const DEFAULT_STATES = "rest,hover,focus-visible,active,expanded,collapsed,quiz-open,quiz-closed,reduced-motion,print";
const USAGE = `visual-qa.mjs

Usage:
  node tests/visual-qa.mjs --help
  node tests/visual-qa.mjs --sample <html> --viewports 1280,768,390 --states ${DEFAULT_STATES} --out <dir>
  node tests/visual-qa.mjs --sample-dir .omo/evidence/design-next/out

This harness drives a real Playwright browser, captures fresh screenshot evidence,
and writes browser-visual-qa-report.json with objective layout/state metrics.`;

function parseArgs(argv) {
  const args = { sample: [] };
  for (let i = 0; i < argv.length; i += 1) {
    const token = argv[i];
    if (!token.startsWith("--")) continue;
    const key = token.slice(2);
    if (key === "help") {
      args.help = true;
      continue;
    }
    const values = [];
    while (argv[i + 1] && !argv[i + 1].startsWith("--")) {
      values.push(argv[++i]);
    }
    const value = values.length ? values.join(" ") : "true";
    if (key === "sample") {
      args.sample.push(...values);
    } else {
      args[key] = value;
    }
  }
  return args;
}

function parseList(value, fallback) {
  return (value || fallback).split(",").map((item) => item.trim()).filter(Boolean);
}

function viewportFor(widthToken) {
  const width = Number.parseInt(widthToken, 10);
  if (!Number.isFinite(width) || width < 320) {
    throw new Error(`Invalid viewport width: ${widthToken}`);
  }
  const height = width >= 1200 ? 900 : width >= 700 ? 1000 : 1200;
  return { width, height, label: `${width}x${height}` };
}

function slug(value) {
  return value
    .normalize("NFKD")
    .replace(/[^\w.-]+/g, "-")
    .replace(/^-+|-+$/g, "")
    .slice(0, 90) || "sample";
}

function collectSamples(args) {
  const samples = args.sample.map((item) => resolve(item));
  if (args["sample-dir"]) {
    const dir = resolve(args["sample-dir"]);
    for (const entry of readdirSync(dir)) {
      const fullPath = join(dir, entry);
      if (extname(entry).toLowerCase() === ".html") samples.push(fullPath);
    }
  }
  const unique = [...new Set(samples)];
  const missing = unique.filter((sample) => !existsSync(sample));
  if (missing.length) {
    throw new Error(`Missing sample(s): ${missing.join(", ")}`);
  }
  if (!unique.length) {
    throw new Error("--sample or --sample-dir is required");
  }
  return unique.sort();
}

async function launchBrowser() {
  try {
    return {
      browser: await chromium.launch({ channel: "chrome", headless: true }),
      launchMode: "chrome-channel",
    };
  } catch (chromeError) {
    return {
      browser: await chromium.launch({ headless: true }),
      launchMode: `bundled-chromium (chrome fallback: ${chromeError.message})`,
    };
  }
}

async function gotoSample(page, sample) {
  await page.goto(pathToFileURL(sample).href, { waitUntil: "load" });
  await page.waitForTimeout(250);
}

async function screenshot(page, path, captures, meta) {
  await page.screenshot({ path, fullPage: true });
  captures.push({ path: resolve(path), ...meta });
}

async function collectPageMetrics(page) {
  return page.evaluate(() => {
    const doc = document.documentElement;
    const body = document.body;
    const visible = (el) => {
      const style = getComputedStyle(el);
      const rect = el.getBoundingClientRect();
      return style.display !== "none" && style.visibility !== "hidden" && rect.width > 0 && rect.height > 0;
    };
    const rects = Array.from(document.querySelectorAll(".node"))
      .filter(visible)
      .map((el) => {
        const rect = el.getBoundingClientRect();
        return {
          className: el.className,
          x: rect.x,
          y: rect.y,
          width: rect.width,
          height: rect.height,
        };
      });
    const overlaps = [];
    for (let i = 0; i < rects.length; i += 1) {
      for (let j = i + 1; j < rects.length; j += 1) {
        const a = rects[i];
        const b = rects[j];
        const x = Math.max(0, Math.min(a.x + a.width, b.x + b.width) - Math.max(a.x, b.x));
        const y = Math.max(0, Math.min(a.y + a.height, b.y + b.height) - Math.max(a.y, b.y));
        if (x * y > 12) {
          overlaps.push({ a: a.className, b: b.className, area: Math.round(x * y) });
        }
      }
    }
    const overflowElements = Array.from(document.querySelectorAll("h1, h2, h3, p, li, button, .node-title, .node-sub"))
      .filter((el) => !el.classList.contains("sr-only") && !el.closest(".sr-only"))
      .filter((el) => visible(el) && el.scrollWidth > el.clientWidth + 2)
      .map((el) => ({
        selector: el.className || el.tagName.toLowerCase(),
        text: (el.textContent || "").trim().slice(0, 80),
        scrollWidth: el.scrollWidth,
        clientWidth: el.clientWidth,
      }));
    const active = document.activeElement;
    const focusStyle = active ? getComputedStyle(active) : null;
    return {
      title: document.title,
      viewport: { width: window.innerWidth, height: window.innerHeight },
      scrollWidth: Math.max(doc.scrollWidth, body.scrollWidth),
      clientWidth: doc.clientWidth,
      horizontalOverflow: Math.max(doc.scrollWidth, body.scrollWidth) > doc.clientWidth + 2,
      branchCount: document.querySelectorAll(".node[class*='branch-']").length,
      connectorCount: document.querySelectorAll(".lines line").length,
      placeholderCount: document.body.innerHTML.match(/\{\{[^}]+\}\}/g)?.length || 0,
      pedagogyPanelCount: document.querySelectorAll(".pedagogy").length,
      quizToggleCount: document.querySelectorAll(".quiz-toggle").length,
      overlaps,
      overflowElements,
      activeElement: active ? active.tagName.toLowerCase() : null,
      activeOutline: focusStyle ? {
        outlineStyle: focusStyle.outlineStyle,
        outlineWidth: focusStyle.outlineWidth,
        boxShadow: focusStyle.boxShadow,
      } : null,
    };
  });
}

async function collectReducedMotionMetrics(page) {
  return page.evaluate(() => {
    const elements = Array.from(document.querySelectorAll(".node button, .content, .quiz-toggle, .icon"));
    return elements.map((el) => {
      const style = getComputedStyle(el);
      return {
        selector: el.className || el.tagName.toLowerCase(),
        transitionDuration: style.transitionDuration,
        transitionProperty: style.transitionProperty,
        animationDuration: style.animationDuration,
      };
    });
  });
}

async function collectPrintMetrics(page) {
  return page.evaluate(() => {
    const contents = Array.from(document.querySelectorAll(".content"));
    const quizAnswers = Array.from(document.querySelectorAll(".quiz-a"));
    const hiddenControls = Array.from(document.querySelectorAll(".lines, .icon, .hint, .quiz-toggle"));
    return {
      contentStates: contents.map((el) => {
        const style = getComputedStyle(el);
        return {
          maxHeight: style.maxHeight,
          overflow: style.overflow,
          display: style.display,
          ariaHidden: el.getAttribute("aria-hidden"),
        };
      }),
      quizAnswerStates: quizAnswers.map((el) => {
        const style = getComputedStyle(el);
        return {
          display: style.display,
          ariaHidden: el.getAttribute("aria-hidden"),
          textLength: (el.textContent || "").trim().length,
        };
      }),
      hiddenControlStates: hiddenControls.map((el) => ({
        selector: el.className || el.tagName.toLowerCase(),
        display: getComputedStyle(el).display,
      })),
    };
  });
}

async function driveInteractionStates(page, sampleLabel, viewportLabel, runDir, captures, states) {
  const branchButton = page.locator(".node:not(.center) > button").first();
  if (await branchButton.count() === 0) {
    return { branchStates: "missing branch button" };
  }

  const result = {};
  const branchBox = await branchButton.boundingBox();

  if (states.has("hover")) {
    await branchButton.hover();
    await page.waitForTimeout(100);
    await screenshot(page, join(runDir, `${sampleLabel}-${viewportLabel}-hover.png`), captures, { sampleLabel, viewportLabel, state: "hover" });
  }

  if (states.has("focus-visible")) {
    await branchButton.focus();
    await page.waitForTimeout(100);
    result.focusMetrics = await collectPageMetrics(page);
    await screenshot(page, join(runDir, `${sampleLabel}-${viewportLabel}-focus-visible.png`), captures, { sampleLabel, viewportLabel, state: "focus-visible" });
  }

  if (states.has("active") && branchBox) {
    await page.mouse.move(branchBox.x + branchBox.width / 2, branchBox.y + branchBox.height / 2);
    await page.mouse.down();
    await page.waitForTimeout(80);
    await screenshot(page, join(runDir, `${sampleLabel}-${viewportLabel}-active-pressed.png`), captures, { sampleLabel, viewportLabel, state: "active-pressed" });
    await page.mouse.up();
    await page.waitForTimeout(100);
  } else if (states.has("expanded")) {
    await branchButton.click();
    await page.waitForTimeout(100);
  }

  if (states.has("expanded")) {
    await screenshot(page, join(runDir, `${sampleLabel}-${viewportLabel}-expanded-mid.png`), captures, { sampleLabel, viewportLabel, state: "expanded-mid" });
    await page.waitForTimeout(400);
    result.expandedMetrics = await collectPageMetrics(page);
    await screenshot(page, join(runDir, `${sampleLabel}-${viewportLabel}-expanded-settled.png`), captures, { sampleLabel, viewportLabel, state: "expanded-settled" });
  }

  if (states.has("collapsed")) {
    const expanded = await branchButton.getAttribute("aria-expanded");
    if (expanded !== "true") await branchButton.click();
    await page.waitForTimeout(100);
    await branchButton.click();
    await page.waitForTimeout(350);
    result.collapsedMetrics = await collectPageMetrics(page);
    await screenshot(page, join(runDir, `${sampleLabel}-${viewportLabel}-collapsed.png`), captures, { sampleLabel, viewportLabel, state: "collapsed" });
  }

  const quizNode = page.locator(".node:has(.quiz-toggle)").first();
  if (await quizNode.count() > 0 && (states.has("quiz-open") || states.has("quiz-closed"))) {
    const quizBranchButton = quizNode.locator("> button");
    const quizExpanded = await quizBranchButton.getAttribute("aria-expanded");
    if (quizExpanded !== "true") {
      await quizBranchButton.click();
      await page.waitForTimeout(450);
    }
    const quizToggle = quizNode.locator(".quiz-toggle").first();
    if (states.has("quiz-open")) {
      await quizToggle.click();
      await page.waitForTimeout(250);
      result.quizOpenMetrics = await collectPageMetrics(page);
      await screenshot(page, join(runDir, `${sampleLabel}-${viewportLabel}-quiz-open.png`), captures, { sampleLabel, viewportLabel, state: "quiz-open" });
    }
    if (states.has("quiz-closed")) {
      const quizState = await quizToggle.getAttribute("aria-expanded");
      if (quizState !== "true") await quizToggle.click();
      await page.waitForTimeout(150);
      await quizToggle.click();
      await page.waitForTimeout(250);
      result.quizClosedMetrics = await collectPageMetrics(page);
      await screenshot(page, join(runDir, `${sampleLabel}-${viewportLabel}-quiz-closed.png`), captures, { sampleLabel, viewportLabel, state: "quiz-closed" });
    }
  }

  return result;
}

function evaluateReport(report) {
  const failures = [];
  for (const sample of report.samples) {
    for (const check of sample.checks) {
      if (check.metrics?.horizontalOverflow) failures.push(`${check.id}: horizontal overflow`);
      if (check.metrics?.placeholderCount) failures.push(`${check.id}: unresolved placeholders`);
      if (check.metrics?.branchCount < 1) failures.push(`${check.id}: no branch nodes`);
      if (check.metrics?.overlaps?.length) failures.push(`${check.id}: node overlaps detected`);
      if (check.metrics?.overflowElements?.length) failures.push(`${check.id}: text element overflow`);
      if (check.interactions?.focusMetrics?.activeOutline) {
        const outline = check.interactions.focusMetrics.activeOutline;
        const hasOutline = outline.outlineStyle !== "none" && outline.outlineWidth !== "0px";
        const hasShadow = outline.boxShadow && outline.boxShadow !== "none";
        if (!hasOutline && !hasShadow) failures.push(`${check.id}: focus-visible style not detected`);
      }
      if (check.printMetrics) {
        const hiddenContent = check.printMetrics.contentStates.some((state) => state.maxHeight !== "none" || state.overflow === "hidden");
        if (hiddenContent) failures.push(`${check.id}: print content not fully expanded`);
        const hiddenAnswer = check.printMetrics.quizAnswerStates.some((state) => state.textLength > 0 && state.display === "none");
        if (hiddenAnswer) failures.push(`${check.id}: print quiz answer remains hidden`);
      }
    }
  }
  return { verdict: failures.length ? "FAIL" : "PASS", failures };
}

async function run() {
  const args = parseArgs(process.argv.slice(2));
  if (args.help) {
    console.log(USAGE);
    return;
  }

  const samples = collectSamples(args);
  const viewports = parseList(args.viewports, DEFAULT_VIEWPORTS).map(viewportFor);
  const states = new Set(parseList(args.states, DEFAULT_STATES));
  const outDir = resolve(args.out || DEFAULT_OUT_DIR);
  const runId = new Date().toISOString().replace(/[:.]/g, "-");
  const runDir = join(outDir, runId);
  mkdirSync(runDir, { recursive: true });

  const { browser, launchMode } = await launchBrowser();
  const report = {
    generatedAt: new Date().toISOString(),
    launchMode,
    sourceMtimeNote: "Screenshots in this report were captured by this run after the latest template edit known to the executor.",
    requestedViewports: viewports,
    requestedStates: [...states],
    runDir: resolve(runDir),
    samples: [],
  };

  try {
    for (let sampleIndex = 0; sampleIndex < samples.length; sampleIndex += 1) {
      const sample = samples[sampleIndex];
      const sampleLabel = `${String(sampleIndex + 1).padStart(2, "0")}-${slug(basename(sample, ".html"))}`;
      const sampleReport = { sample: resolve(sample), sampleLabel, checks: [] };
      report.samples.push(sampleReport);

      for (const viewport of viewports) {
        const context = await browser.newContext({
          viewport: { width: viewport.width, height: viewport.height },
          reducedMotion: "no-preference",
          colorScheme: "light",
        });
        const page = await context.newPage();
        await gotoSample(page, sample);
        const captures = [];
        const id = `${sampleLabel}-${viewport.label}`;

        if (states.has("rest")) {
          await screenshot(page, join(runDir, `${id}-rest.png`), captures, { sampleLabel, viewportLabel: viewport.label, state: "rest" });
        }
        const metrics = await collectPageMetrics(page);
        const interactions = await driveInteractionStates(page, sampleLabel, viewport.label, runDir, captures, states);
        sampleReport.checks.push({ id, viewport, media: "screen", metrics, interactions, captures });
        await context.close();

        if (states.has("reduced-motion")) {
          const reducedContext = await browser.newContext({
            viewport: { width: viewport.width, height: viewport.height },
            reducedMotion: "reduce",
            colorScheme: "light",
          });
          const reducedPage = await reducedContext.newPage();
          await gotoSample(reducedPage, sample);
          const reducedCaptures = [];
          await screenshot(reducedPage, join(runDir, `${id}-reduced-motion.png`), reducedCaptures, { sampleLabel, viewportLabel: viewport.label, state: "reduced-motion" });
          sampleReport.checks.push({
            id: `${id}-reduced-motion`,
            viewport,
            media: "screen",
            reducedMotion: true,
            metrics: await collectPageMetrics(reducedPage),
            reducedMotionMetrics: await collectReducedMotionMetrics(reducedPage),
            captures: reducedCaptures,
          });
          await reducedContext.close();
        }
      }

      if (states.has("print")) {
        const printViewport = viewportFor("1280");
        const printContext = await browser.newContext({
          viewport: { width: printViewport.width, height: printViewport.height },
          reducedMotion: "reduce",
          colorScheme: "light",
        });
        const printPage = await printContext.newPage();
        await printPage.emulateMedia({ media: "print", reducedMotion: "reduce" });
        await gotoSample(printPage, sample);
        const printCaptures = [];
        await screenshot(printPage, join(runDir, `${sampleLabel}-${printViewport.label}-print.png`), printCaptures, { sampleLabel, viewportLabel: printViewport.label, state: "print" });
        sampleReport.checks.push({
          id: `${sampleLabel}-${printViewport.label}-print`,
          viewport: printViewport,
          media: "print",
          metrics: await collectPageMetrics(printPage),
          printMetrics: await collectPrintMetrics(printPage),
          captures: printCaptures,
        });
        await printContext.close();
      }
    }
  } finally {
    await browser.close();
  }

  report.summary = evaluateReport(report);
  const reportPath = resolve(dirname(runDir), "browser-visual-qa-report.json");
  writeFileSync(reportPath, `${JSON.stringify(report, null, 2)}\n`, "utf8");
  writeFileSync(resolve(runDir, "visual-qa-request.json"), `${JSON.stringify({
    samples,
    viewports,
    states: [...states],
    reportPath,
    runDir: resolve(runDir),
  }, null, 2)}\n`, "utf8");
  console.log(`[visual-qa] ${report.summary.verdict}`);
  console.log(`[visual-qa] report: ${reportPath}`);
  console.log(`[visual-qa] screenshots: ${resolve(runDir)}`);
  if (report.summary.failures.length) {
    for (const failure of report.summary.failures) console.log(`- ${failure}`);
    process.exit(1);
  }
}

run().catch((error) => {
  console.error(error.stack || error.message);
  process.exit(1);
});
