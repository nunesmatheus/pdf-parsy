# frozen_string_literal: true

require 'rails_helper'

RSpec.describe TextFromPdfService do
  context 'when pdf does not have columns' do
    let(:one_column_lines) do
      [
        '02 - O Brasil apresenta uma situação confortável, em termos globais, quanto aos recursos hídricos. A disponibilidade hídrica per',
        'capita, determinada a partir de valores totalizados para o País, indica uma situação satisfatória [...]. Entretanto, apesar desse',
        'aparente conforto, existe uma distribuição espacial desigual dos recursos hídricos no território brasileiro. [...] O conhecimento',
        'da distribuição espacial da precipitação e, consequentemente, o da oferta de água, é de fundamental importância para',
        'determinar o balanço hídrico nas bacias brasileiras.'
      ]
    end

    let(:file) do
      Rack::Test::UploadedFile.new(
        Rails.root.join('spec/fixtures/files/UFPR-2015.pdf')
      )
    end

    let(:service) { described_class.new(file.path) }

    it 'lines are all concatenated' do
      text = service.call
      lines = text.split("\n")
      index = lines.find_index(one_column_lines[0])
      one_column_lines[1..-1].each_with_index do |_line, i|
        expect(lines[index + i].strip).to eq one_column_lines[i].strip
      end
    end
  end

  context 'when pdf has columns' do
    let(:left_column_lines) do
      [
        'A figura exemplifica o comportamento de povos indígenas que',
        'viveram no Brasil há 1.000 anos. Eles construíam suas casas',
        'escavadas na terra, faziam fogueiras e manuseavam objetos.'
      ]
    end

    let(:right_column_lines) do
      [
        'No planeta Terra, há processos escultores, tais como a ação do',
        'gelo, o intemperismo e a ação do vento. A atuação de tais',
        'processos pode ser representada em gráficos elaborados'
      ]
    end

    let(:file) do
      Rack::Test::UploadedFile.new(
        Rails.root.join('spec/fixtures/files/fuvest-2018.pdf')
      )
    end

    let(:service) { described_class.new(file.path) }

    it 'left column lines are concatenated with right columns lines' do
      text = service.call
      lines = text.split("\n").map(&:strip)
      index = lines.find_index(left_column_lines[0])
      left_column_lines[1..-1].each_with_index do |_line, i|
        expect(lines[index + i]).to eq left_column_lines[i]
      end

      index = lines.find_index(right_column_lines[0])
      right_column_lines[1..-1].each_with_index do |_line, i|
        expect(lines[index + i]).to eq right_column_lines[i]
      end
    end
  end
end
