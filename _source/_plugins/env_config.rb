module Jekyll
	class EnvironmentConfigGenerator < Generator
		# Default environment configuration
		DEFAULTS = {
			'environment' => 'development'
		}
		
		def generate(site)
			file = File.join(Dir.pwd, "_env.yml")
			site.config['environment'] = read_config_file(file)['environment']
      Jekyll.logger.info "Environment:", site.config['environment']
		end
		
		def read_config_file(file)
      env_config = YAML.safe_load_file(file)
      raise ArgumentError.new("Environment Configuration file: (INVALID) #{file}".yellow) if !env_config.is_a?(Hash)
      Jekyll.logger.info "Environment file:", file
      env_config
    rescue SystemCallError
      Jekyll.logger.warn "Environment file:", "none"
			DEFAULTS	
		end
	end
end
