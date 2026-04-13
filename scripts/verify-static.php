<?php

declare(strict_types=1);

require_once __DIR__ . '/../vendor/autoload.php';

/**
 * Verification Script
 * Compares generated static JSON files with the output from the live engine.
 */

function verifyJson(string $staticFile, array $expectedData): bool {
    if (!file_exists($staticFile)) {
        echo "FAIL: File missing: $staticFile\n";
        return false;
    }

    $actualJson = file_get_contents($staticFile);
    $actualData = json_decode($actualJson, true);

    if ($actualData === null) {
        echo "FAIL: Invalid JSON in $staticFile\n";
        return false;
    }

    // Remove volatile metadata before comparison
    unset($expectedData['metadata']['generation_time']);
    unset($actualData['metadata']['generation_time']);
    unset($expectedData['metadata']['request_id']);
    unset($actualData['metadata']['request_id']);

    if ($expectedData === $actualData) {
        echo "PASS: $staticFile matches engine output.\n";
        return true;
    } else {
        echo "FAIL: Mismatch in $staticFile\n";
        // Optional: save a diff or log details
        return false;
    }
}

// Example usage would involve looping through the same logic as the generator
// and comparing instead of writing.
echo "Verification logic ready. Run after generation.\n";
