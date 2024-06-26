from flask import Flask, render_template, request, send_file, redirect, url_for
from docx import Document
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/escolher_contrato', methods=['GET', 'POST'])
def escolher_contrato():
    if request.method == 'POST':
        tipo_contrato = request.form['tipo_contrato']
        return render_template('form.html', tipo_contrato=tipo_contrato)
    return render_template('escolher_contrato.html')

@app.route('/gerar_contrato_compra_venda', methods=['POST'])
def gerar_contrato_compra_venda():
    if request.method == 'POST':
        # Carregar o modelo do documento
        template_path = 'documentos/modelo_compra_venda.docx'
        document = Document(template_path)

        # Dados do formulário
        dados_formulario = {
            'nome_vendedor': request.form['nome_vendedor'],
            'nacionalidade_vendedor': request.form['nacionalidade_vendedor'],
            'estado_civil_vendedor': request.form['estado_civil_vendedor'],
            'profissao_vendedor': request.form['profissao_vendedor'],
            'cpf_vendedor': request.form['cpf_vendedor'],
            'endereco_vendedor': request.form['endereco_vendedor'],
            'nome_comprador': request.form['nome_comprador'],
            'estado_civil_comprador': request.form['estado_civil_comprador'],
            'profissao_comprador': request.form['profissao_comprador'],
            'cpf_comprador': request.form['cpf_comprador'],
            'endereco_comprador': request.form['endereco_comprador'],
            'descricao_detalhada_do_bem': request.form['descricao_detalhada_do_bem'],
            'endereco_imovel': request.form['endereco_imovel'],
            'valor_venda': request.form['valor_venda'],
            'condicoes_pagamento': request.form['condicoes_pagamento'],
            'data_de_entrega': request.form['data_de_entrega'],
            'percentual': request.form['percentual'],
            'cidade_contrato': request.form['cidade_contrato'],
            'data_contrato': request.form['data_contrato'],
        }

        # Substituir os espaços reservados pelos dados do formulário
        for paragraph in document.paragraphs:
            for key, value in dados_formulario.items():
                if key in paragraph.text:
                    paragraph.text = paragraph.text.replace(f'[{key}]', value)

        # Nome do arquivo de saída
        output_path = 'documentos/contrato_compra_venda.docx'

        # Salvar o documento gerado
        document.save(output_path)

        # Redirecionar para a página de download
        return redirect(url_for('download_contrato', filename='contrato_compra_venda.docx'))

@app.route('/download_contrato/<filename>')
def download_contrato(filename):
    return render_template('download_contrato.html', filename=filename)

@app.route('/baixar_contrato/<filename>')
def baixar_contrato(filename):
    filepath = f'documentos/{filename}'
    return send_file(filepath, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
