# frozen_string_literal: true

require 'swagger_helper'

RSpec.describe PdfToTextController do
  describe '#create' do
    path '/pdf_to_text' do
      parameter name: :file, in: :formData, type: :file, format: :binary, required: true

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

        post('successful') do
          produces 'multipart/form-data'
          consumes 'multipart/form-data'
          tags 'PdfToText'

          response(200, 'successful') do
            let(:file) do
              Rack::Test::UploadedFile.new(Rails.root.join('spec/fixtures/files/UFPR-2015.pdf'))
            end

            run_test! do
              lines = json_body[:text].split("\n")
              index = lines.find_index(one_column_lines[0])
              one_column_lines[1..-1].each_with_index do |_line, i|
                expect(lines[index + i].strip).to eq one_column_lines[i].strip
              end
            end
          end
        end
      end
    end
  end
end
