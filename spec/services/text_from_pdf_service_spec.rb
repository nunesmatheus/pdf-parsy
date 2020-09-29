# frozen_string_literal: true

require 'rails_helper'

RSpec.describe TextFromPdfService do
  context 'when pdf does not have columns' do
    let(:one_column_line) do
      '02 - O Brasil apresenta uma situação confortável, em termos globais, quanto aos recursos hídricos. A disponibilidade hídrica per capita, determinada a partir de valores totalizados para o País, indica uma situação satisfatória [...]. Entretanto, apesar desse aparente conforto, existe uma distribuição espacial desigual dos recursos hídricos no território brasileiro. [...] O conhecimento da distribuição espacial da precipitação e, consequentemente, o da oferta de água, é de fundamental importância para determinar o balanço hídrico nas bacias brasileiras.'
    end

    let(:file) do
      Rack::Test::UploadedFile.new(
        Rails.root.join('spec/fixtures/files/UFPR-2015.pdf')
      )
    end

    let(:service) { described_class.new(file.path) }

    it 'lines are all concatenated' do
      text = service.call
      expect(text).to include one_column_line
    end
  end

  context 'when pdf has columns' do
    let(:left_column_line) do
      'A figura exemplifica o comportamento de povos indígenas que viveram no Brasil há 1.000 anos. Eles construíam suas casas escavadas na terra, faziam fogueiras e manuseavam objetos.'
    end

    let(:right_column_line) do
      'No planeta Terra, há processos escultores, tais como a ação do gelo, o intemperismo e a ação do vento. A atuação de tais processos pode ser representada em gráficos elaborados'
    end

    let(:file) do
      Rack::Test::UploadedFile.new(
        Rails.root.join('spec/fixtures/files/fuvest-2018.pdf')
      )
    end

    let(:service) { described_class.new(file.path) }

    it 'left column lines are concatenated with right columns lines' do
      text = service.call
      expect(text).to include left_column_line
      expect(text).to include right_column_line
    end
  end
end
