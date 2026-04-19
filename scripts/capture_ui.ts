#!/usr/bin/env ts-node
/**
 * UI Capture Tool
 *
 * Captures the current UI state for Agent understanding:
 * 1. Takes a screenshot of the page
 * 2. Extracts the accessibility tree (DOM structure as text)
 *
 * This allows the Agent to "see" the UI through text-based representation.
 */

import { chromium, Browser, Page } from 'playwright';
import * as fs from 'fs';
import * as path from 'path';

const DEV_SERVER_URL = 'http://localhost:5173';
const LOGS_DIR = path.join(process.cwd(), 'logs');
const SCREENSHOT_PATH = path.join(LOGS_DIR, 'screenshot.png');
const UI_STRUCTURE_PATH = path.join(LOGS_DIR, 'ui_structure.txt');

// Ensure logs directory exists
if (!fs.existsSync(LOGS_DIR)) {
  fs.mkdirSync(LOGS_DIR, { recursive: true });
}

/**
 * Format accessibility tree node into readable text
 */
function formatAccessibilityTree(node: any, indent: string = ''): string {
  if (!node) return '';

  let result = '';
  const role = node.role || 'unknown';
  const name = node.name || '';
  const value = node.value || '';
  const description = node.description || '';

  // Format the node
  result += `${indent}[${role}]`;
  if (name) result += ` name="${name}"`;
  if (value) result += ` value="${value}"`;
  if (description) result += ` description="${description}"`;
  result += '\n';

  // Process children recursively
  if (node.children && node.children.length > 0) {
    for (const child of node.children) {
      result += formatAccessibilityTree(child, indent + '  ');
    }
  }

  return result;
}

/**
 * Main capture function
 */
async function captureUI() {
  let browser: Browser | null = null;

  try {
    console.log('==========================================');
    console.log('UI Capture Tool');
    console.log('==========================================\n');

    console.log(`Connecting to dev server at ${DEV_SERVER_URL}...`);

    // Launch browser
    console.log('Launching browser...');
    browser = await chromium.launch({
      headless: true,
      timeout: 30000
    });

    const context = await browser.newContext({
      viewport: { width: 1280, height: 720 }
    });
    const page = await context.newPage();

    // Navigate to the page
    console.log(`Navigating to ${DEV_SERVER_URL}...`);
    try {
      await page.goto(DEV_SERVER_URL, {
        waitUntil: 'networkidle',
        timeout: 10000
      });
      console.log('✓ Page loaded successfully\n');
    } catch (error) {
      console.error('✗ Failed to connect to dev server.');
      console.error('  Make sure the dev server is running: npm run dev');
      process.exit(1);
    }

    // Take screenshot
    console.log('Capturing screenshot...');
    await page.screenshot({
      path: SCREENSHOT_PATH,
      fullPage: true
    });
    console.log(`✓ Screenshot saved: ${SCREENSHOT_PATH}`);

    // Extract accessibility tree
    console.log('\nExtracting accessibility tree...');
    const snapshot = await page.accessibility.snapshot();

    if (!snapshot) {
      console.error('✗ Failed to get accessibility snapshot');
      process.exit(1);
    }

    // Format and save accessibility tree
    const formattedTree = formatAccessibilityTree(snapshot);
    fs.writeFileSync(UI_STRUCTURE_PATH, formattedTree, 'utf-8');
    console.log(`✓ UI structure saved: ${UI_STRUCTURE_PATH}`);

    // Display preview
    console.log('\n==========================================');
    console.log('UI Structure Preview:');
    console.log('==========================================');
    const lines = formattedTree.split('\n').slice(0, 30);
    console.log(lines.join('\n'));
    if (formattedTree.split('\n').length > 30) {
      console.log('\n... (truncated, see ui_structure.txt for full output)');
    }
    console.log('\n==========================================');
    console.log('✓ UI capture completed successfully');
    console.log('==========================================\n');

  } catch (error) {
    console.error('\n✗ Error during UI capture:');
    if (error instanceof Error) {
      console.error(`  ${error.message}`);
    } else {
      console.error(error);
    }
    process.exit(1);
  } finally {
    if (browser) {
      await browser.close();
    }
  }
}

// Run the capture
captureUI();
