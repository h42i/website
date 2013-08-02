module Jekyll
	class EnvironmentConfigGenerator < Generator
		def generate(site)
			file = File.join(Dir.pwd, "_env.yml")
    	env_config = YAML.safe_load_file(file)
      raise ArgumentError.new("Environment Configuration file: (INVALID) #{file}".yellow) if !env_config.is_a?(Hash)
      Jekyll.logger.info "Environment Configuration file:", file
			site.config['env'] = env_config
		rescue SystemCallError
			Jekyll.logger.warn "Environment Configuration file:", "none"
		end
	end
end
