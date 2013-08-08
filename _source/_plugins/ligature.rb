module Jekyll
	class LigatureConverter < Converter
		safe true
		priority :medium
		
		def matches(ext)
			ext =~ /^\.markdown$/i
		end

		def output_ext(ext)
			'.markdown'
		end

		def convert(content)
			content.upcase
		end
	end
end
