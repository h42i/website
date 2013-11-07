class Calendar < Liquid::Tag
  Syntax = /^\s*([^\s]+)(\s+([^"\s]+)\s*)?/

  def initialize(tagName, markup, tokens)
    super

    if markup =~ Syntax then
      @type = "#{$1}"

      if $2.nil? then
          @src = ""
      else
          @src = "#{$3}\" "
      end
    else
      raise "Invalid Syntax for calendar tag"
    end
  end

  def render(context)
    "<!-- ical #{@type} #{@src}--><!-- /ical -->"
  end

  Liquid::Template.register_tag "ical", self
end
