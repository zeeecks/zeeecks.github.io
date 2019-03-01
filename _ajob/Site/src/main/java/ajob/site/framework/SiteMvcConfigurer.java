package ajob.site.framework;

import org.springframework.context.annotation.Configuration;
import org.springframework.web.servlet.config.annotation.InterceptorRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;

import ajob.site.framework.interceptor.AuthInterceptor;
import ajob.site.framework.interceptor.EncodingInterceptor;

/**
 * MVC的配置操作
 * @author cqchen 2018年5月9日14:43:01
 *
 */
@Configuration
public class SiteMvcConfigurer implements WebMvcConfigurer {

	/**
	 * 添加拦截器配置
	 */
	@Override
	public void addInterceptors(InterceptorRegistry registry) {
		registry.addInterceptor(new EncodingInterceptor()).addPathPatterns("/**");
		registry.addInterceptor(new AuthInterceptor()).addPathPatterns("/**");
	}
	
}
