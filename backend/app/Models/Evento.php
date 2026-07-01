<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class Evento extends Model
{
    use HasFactory;

    protected $fillable = [
        'nome_evento',
        'tipo_evento',
        'data_evento',
        'endereco_evento',
        'orcamento_evento',
    ];

    protected $table = 'eventos';
}
