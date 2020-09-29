# frozen_string_literal: true

module RequestMacros
  def json_body
    JSON.parse(@response.body, symbolize_names: true)
  rescue JSON::ParserError
    @response.body
  end
end
