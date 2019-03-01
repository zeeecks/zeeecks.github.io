package ajob.site.framework;

import java.util.Collections;

import javax.servlet.ServletContext;
import javax.servlet.ServletException;
import javax.servlet.SessionTrackingMode;

import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.builder.SpringApplicationBuilder;
import org.springframework.boot.web.servlet.support.SpringBootServletInitializer;

/**
 * Servlet初始化操作
 * @author cqchen 2018年5月9日14:49:40
 *
 */
public class SiteServletInitializer extends SpringBootServletInitializer {

	@Override
	public void onStartup(ServletContext servletContext) throws ServletException {

		super.onStartup(servletContext);
		
		//设置session的追踪模式为cookie，这样子就不会导致jessionId出现在url后面
		servletContext.setSessionTrackingModes(Collections.singleton(SessionTrackingMode.COOKIE));
		servletContext.getSessionCookieConfig().setHttpOnly(true);
	}
	
	@Override
	protected SpringApplicationBuilder configure(SpringApplicationBuilder builder) {
		return builder.sources(SpringBootApplication.class);
	}
}
