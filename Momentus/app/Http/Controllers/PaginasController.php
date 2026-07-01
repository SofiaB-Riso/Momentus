<?php

namespace App\Http\Controllers;

use App\Models\Evento;
use Illuminate\Http\Request;

class PaginasController extends Controller
{
    public function index(){
        $eventos = Evento::all();
        return view('paginas.index', compact('eventos'));
    }

    public function create(){
        $eventos = Evento::all();
        return view('paginas.criar-evento', compact('eventos'));
    }

    public function store(Request $request){
        Evento::create([
            'nome_evento'=>$request->nome_evento,
            'tipo_evento'=>$request->tipo_evento,
            'data_evento'=>$request->data_evento,
            'endereco_evento'=>$request->endereco_evento,
            'orcamento_evento'=>$request->orcamento_evento,
        ]);

        return redirect()->route('eventos.index');
    }

    public function show(Evento $evento){
        return view('paginas.mostrar-evento', compact('evento'));
    }

    public function edit($id)
    {
        $evento = Evento::findOrFail($id);

        return view('paginas.editar-evento', compact('evento'));
    }

    public function update(Request $request, $id)
    {
        $evento = Evento::findOrFail($id);
        

        $evento->update([
            'nome_evento'=>$request->nome_evento,
            'tipo_evento'=>$request->tipo_evento,
            'data_evento'=>$request->data_evento,
            'endereco_evento'=>$request->endereco_evento,
            'orcamento_evento'=>$request->orcamento_evento,
        ]);
        return redirect()->route('eventos.index');
    }

    public function destroy($id)
    {
        $evento = Evento::findOrFail($id);

        $evento->delete();
        return redirect()->route("eventos.index")
            ->with("successo", "O evento $evento->nome_evento foi deletado.");
    }

}
