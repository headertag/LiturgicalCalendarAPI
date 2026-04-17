<?php

declare(strict_types=1);

require_once __DIR__ . '/../vendor/autoload.php';

use LiturgicalCalendar\Api\Handlers\CalendarHandler;
use LiturgicalCalendar\Api\Handlers\MetadataHandler;
use LiturgicalCalendar\Api\Enum\JsonData;
use LiturgicalCalendar\Api\Utilities;
use LiturgicalCalendar\Api\Router;
use Nyholm\Psr7\ServerRequest;
use Dotenv\Dotenv;

// Setup environment
$projectFolder = dirname(__DIR__);
$dotenv = Dotenv::createImmutable($projectFolder, ['.env', '.env.local', '.env.development', '.env.test', '.env.staging', '.env.production'], false);
$dotenv->safeLoad();

// Setup constants
ini_set('date.timezone', 'Europe/Vatican');
Router::getApiPaths();

// Output directory
$distPath = $projectFolder . DIRECTORY_SEPARATOR . 'dist' . DIRECTORY_SEPARATOR . 'v1';
if (!file_exists($distPath)) {
    mkdir($distPath, 0755, true);
}

/**
 * Generate a static calendar file for a given year, nation/diocese, and locale.
 */
function generateCalendar(int $year, ?string $nation, ?string $diocese, string $locale, string $outputFile): void {
    if (file_exists($outputFile)) {
        // Skip for now to save time in prototyping
        // return;
    }

    $queryParams = [
        'year'   => (string) $year,
        'locale' => $locale
    ];

    if ($nation !== null) {
        $queryParams['national_calendar'] = $nation;
    }
    if ($diocese !== null) {
        $queryParams['diocesan_calendar'] = $diocese;
    }

    $request = new ServerRequest('GET', '/calendar', [], null, '1.1', [
        'QUERY_STRING' => http_build_query($queryParams)
    ]);
    $request = $request->withQueryParams($queryParams);

    try {
        $handler = new CalendarHandler();
        $response = $handler->handle($request);
        
        $dir = dirname($outputFile);
        if (!file_exists($dir)) {
            mkdir($dir, 0755, true);
        }
        
        file_put_contents($outputFile, (string) $response->getBody());
        echo "Generated: $outputFile\n";
    } catch (\Throwable $e) {
        echo "Error generating $year - " . ($nation ?? $diocese) . " ($locale): " . $e->getMessage() . "\n";
    }
}

// 1. Get Metadata
echo "Building Metadata...\n";
// We need to bypass some of the HTTP-specific logic in MetadataHandler if possible,
// or just use the same logic it uses.
$metadataFile = $projectFolder . DIRECTORY_SEPARATOR . 'dist' . DIRECTORY_SEPARATOR . 'metadata.json';
$metadataHandler = new MetadataHandler();
$metadataRequest = new ServerRequest('GET', '/metadata');
$metadataResponse = $metadataHandler->handle($metadataRequest);
$metadataJson = (string) $metadataResponse->getBody();
file_put_contents($metadataFile, $metadataJson);
$metadata = json_decode($metadataJson, true)['litcal_metadata'];

$years = [2025, 2026]; // Just for prototyping
$locales = ['en', 'it', 'la']; // Common locales

// 2. Generate National Calendars
echo "Generating National Calendars...\n";
foreach ($years as $year) {
    foreach ($metadata['national_calendars'] as $calendar) {
        $nation = $calendar['calendar_id'];
        foreach ($calendar['locales'] as $localeFull) {
            $locale = explode('_', $localeFull)[0]; // Use base locale
            if (!in_array($locale, $locales)) continue;
            
            $outputFile = "$distPath/$year/nations/$nation/$locale.json";
            generateCalendar($year, $nation, null, $locale, $outputFile);
        }
    }
}

// 3. Generate Diocesan Calendars
echo "Generating Diocesan Calendars...\n";
foreach ($years as $year) {
    foreach ($metadata['diocesan_calendars'] as $calendar) {
        $diocese = $calendar['calendar_id'];
        $nation = null; // Handler will derive nation from diocese ID
        foreach ($calendar['locales'] as $localeFull) {
            $locale = explode('_', $localeFull)[0];
            if (!in_array($locale, $locales)) continue;

            $outputFile = "$distPath/$year/dioceses/$diocese/$locale.json";
            generateCalendar($year, null, $diocese, $locale, $outputFile);
        }
    }
}

echo "Done!\n";
