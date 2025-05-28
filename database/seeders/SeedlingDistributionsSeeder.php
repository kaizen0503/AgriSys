<?php

namespace Database\Seeders;

use Illuminate\Database\Console\Seeds\WithoutModelEvents;
use Illuminate\Database\Seeder;
use Illuminate\Support\Facades\DB;
use Carbon\Carbon;

class SeedlingDistributionsSeeder extends Seeder
{
   
public function run()
{
    $start = Carbon::parse('2022-01-01');
    for ($i = 0; $i < 36; $i++) {
        DB::table('seedling_distributions')->insert([
            'distribution_date' => $start->copy()->addMonths($i)->toDateString(),
            'quantity' => rand(800, 1500) + (int)(200 * sin($i / 6)), // simulate seasonality
            'location' => 'Barangay '.chr(65 + ($i % 5)),
            'created_at' => now(),
            'updated_at' => now(),
        ]);
    }
}
}
