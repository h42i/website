require 'uri'

module Jekyll
  module OctopodFilters
    JSON_ENTITIES = { '&' => '\u0026', '>' => '\u003E', '<' => '\u003C', "'" => '\u0027' }

    # Escapes  some text for CDATA
    def cdata_escape(input)
      input.gsub(/<!\[CDATA\[/, '&lt;![CDATA[').gsub(/\]\]>/, ']]&gt;')
    end

    # Escapes HTML entities in JSON strings.
    # More or less a copy of the equivalent method in Active Support.
    # https://github.com/rails/rails/tree/master/activesupport
    def j(str)
      str.to_s.gsub(/[&"><']/) { |e| JSON_ENTITIES[e] }
    end

    # Replaces relative urls with full urls
    #
    #   {{ "about.html" | expand_urls }}             => "/about.html"
    #   {{ "about.html" | expand_urls:site.url }}  => "http://example.com/about.html"
    def expand_urls(input, url='')
      url ||= '/'
      input.gsub /(\s+(href|src)\s*=\s*["|']{1})(\/[^\"'>]*)/ do
        $1+url+$3
      end
    end

    # Formats a Time to be RSS compatible like "Wed, 15 Jun 2005 19:00:00 GMT"
    #
    #   {{ site.time | time_to_rssschema }}
    def time_to_rssschema(time)
      time.strftime("%a, %d %b %Y %H:%M:%S %z")
    end

    # Returns the first argument if it's not nil or empty otherwise it returns
    # the second one.
    #
    #   {{ post.author | otherwise:site.author }}
    def otherwise(first, second)
      first = first.to_s
      first.empty? ? second : first
    end

    # Returns the value of a given hash. Is no key as second parameter given, it
    # trys first "mp3", than "m4a" and than it will return a more or less random
    # value.
    #
    #   {{ post.audio | audio:"m4a" }} => "my-episode.m4a"
    def audio(hsh, key = nil)
      if key.nil?
        hsh['mp3'] ? hsh['mp3'] : hsh['m4a'] ? hsh['m4a'] : hsh.values.first
      else
        hsh[key]
      end
    end

    # Returns the size of a given file in bytes. If there is just a filename
    # without a path, this method assumes that the file is an episode audio file
    # which lives in /episodes.
    #
    #   {{ "example.m4a" | file_size }} => 4242
    def file_size(path, rel = nil)
      return 0 if path.nil?
      path = path =~ /\// ? path : File.join('episodes', path)
      path = rel + path if rel
      File.size(path)
    end

    # Returns a slug based on the id of a given page.
    #
    #   {{ page | slug }} => '2012_10_02_octopod'
    def slug(page)
      page['id'][1..-1].gsub('/', '_')
    end

    # Splits a chapter, like it is written to the post YAML front matter into
    # the components 'start' which refers to a single point in time relative to
    # the beginning of the media file nad 'title' which defines the text to be
    # the title of the chapter.
    #
    #   {{ '00:00:00.000 Welcome to Octopod!' | split_chapter }}
    #     => { 'start' => '00:00:00.000', 'title' => 'Welcome to Octopod!' }
    #
    #   {{ '00:00:00.000 Welcome to Octopod!' | split_chapter:'title' }}
    #     => 'Welcome to Octopod!'
    #
    #   {{ '00:00:00.000 Welcome to Octopod!' | split_chapter:'start' }}
    #     => '00:00:00.000'
    def split_chapter(chapter_str, attribute = nil)
      attributes = chapter_str.split(/ /, 2)
      return nil unless attributes.first.match(/\A(\d|:|\.)+\z/)

      if attribute.nil?
        { 'start' => attributes.first, 'title' => attributes.last }
      else
        attribute == 'start' ? attributes.first : attributes.last
      end
    end

    # Returns an <audio>-tag for a given page with <source>-tags in it for every
    # audio file in the page's YAML front matter.
    #
    #   {{ page | audio_tag:site }}
    def audio_tag(page, site)
      out = %Q{<audio id="#{slug(page)}_player" preload="none">\n}
      out + page['audio'].map { |format, filename|
        %Q{<source src="#{site['url']}/episodes/#{ERB::Util.url_encode(filename)}" type="#{mime_type(format)}"></source>}
      }.join("\n") + "\n</audio>\n"
    end

    # Returns the web player for the episode of a given page.
    #
    #   {{ page | web_player:site }}
    def web_player(page, site)
      return if page['audio'].nil?

      options = {
        'alwaysShowHours'     => 'true',
        'startVolume'         => '0.8',
        'width'               => 'auto',
        'summaryVisible'      => 'false',
        'timecontrolsVisible' => 'false',
        'chaptersVisible'     => 'true',
        'sharebuttonsVisible' => 'false'
      }

      simple_keys = %w[title alwaysShowHours startVolume width summaryVisible
        timecontrolsVisible chaptersVisible sharebuttonsVisible]

      if site = site.dup
        site.delete('title')
        site.delete('subtitle')
        options = options.merge(site)
      end
      options = options.merge(page)

      out = audio_tag(page, site)
      out << "<script>\n$('##{slug(page)}_player').podlovewebplayer({\n"
      out << "poster: '#{site['url']}#{(options['episode_cover'] || '/img/logo-360x360.png')}',\n"
      out << "subtitle: '#{j(options['subtitle'])}',\n" if options['subtitle']
      out << "chapters: '#{options['chapters'].map { |c| j(c) }.join(%Q{'+"\\n"+'})}',\n" if options['chapters']
      out << "summary: '#{j(options['summary'])}',\n" if options['summary']
      out << "duration: '#{string_of_duration(options['duration'])}',\n"
      out << "permalink: '#{site['url']}#{page['url']}',\n"

      out << simple_keys.map { |k|
        "#{k}: #{(k = options[k].to_s) =~ /\A(true|false|[0-9\.]+)\z/ ? k : "'#{j(k)}'"}"
      }.join(",\n") + "});\n</script>\n"
    end

    # Gets a number of seconds and returns an human readable duration string of
    # it.
    #
    #   {{ 1252251 | string_of_duration }} => "00:03:13"
    def string_of_duration(duration)
      seconds = duration.to_i
      minutes = seconds / 60
      hours   = minutes / 60

      "#{"%02d" % hours}:#{"%02d" % (minutes % 60)}:#{"%02d" % (seconds % 60)}"
    end

    # Gets a number of bytes and returns an human readable string of it.
    #
    #   {{ 1252251 | string_of_size }} => "1.19M"
    def string_of_size(bytes)
      bytes = bytes.to_i.to_f
      out = '0'
      return out if bytes == 0.0

      jedec = %w[b K M G]
      [3, 2, 1, 0].each { |i|
        if bytes > 1024 ** i
          out = "%.1f#{jedec[i]}" % (bytes / 1024 ** i)
          break
        end
      }

      return out
    end

    # Returns the host a given url
    #
    #   {{ 'https://github.com/pattex/octopod' | host_from_url }} => "github.com"
    def host_from_url(url)
      URI.parse(url).host
    end
  end
end

Liquid::Template.register_filter(Jekyll::OctopodFilters)