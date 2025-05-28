<?php

use Illuminate\Support\Facades\Route;
use App\Http\Controllers\AnalyticsController;
// This file is part of the Laravel Seedling Distribution Analytics project.
// It defines the web routes for the application, including the home route and the analytics route.
//
// The home route returns the welcome view, while the analytics route triggers the analytics process
// by calling the run method of the AnalyticsController. The analytics process involves
// fetching seedling distribution data from the database, saving it to a JSON file, and executing
// a Python script to perform further analysis. The output of the analysis is then returned as a JSON file.
Route::get('/', function () {
    return view('welcome');
});



Route::get('/run-analytics', [AnalyticsController::class, 'run']);
