<?php

use App\Http\Controllers\PaginasController;
use Illuminate\Support\Facades\Route;

Route::resource('/eventos', PaginasController::class);
