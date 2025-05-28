<?php
namespace App\Http\Controllers;

use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Log;

class AnalyticsController extends Controller
{
    public function run()
    {
        try {
            Log::info("Step 1: Analytics starting...");

            $data = DB::table('seedling_distributions')
                ->orderBy('distribution_date')
                ->get(['distribution_date as date', 'quantity']);

            Log::info("Step 2: Retrieved data", ['count' => count($data)]);

            $jsonPath = public_path('analytics/input_data.json');
            file_put_contents($jsonPath, json_encode($data, JSON_PRETTY_PRINT));

            Log::info("Step 3: Wrote to input_data.json", ['path' => $jsonPath]);

           $scriptPath = base_path('scripts/analytics.py');  // Laravel helper to get full path to project root + scripts/analytics.py
            $command = "python " . escapeshellarg($scriptPath);
            exec($command, $output, $status);
            Log::info("Step 4: Ran Python script", ['status' => $status, 'output' => $output]);

            return response()->file(public_path('analytics/output.json'));
        } catch (\Exception $e) {
            Log::error("Analytics failed: " . $e->getMessage());
            return response()->json(['error' => 'Analytics failed'], 500);
        }
    }
}
