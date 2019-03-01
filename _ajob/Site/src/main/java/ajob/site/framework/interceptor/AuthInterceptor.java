package ajob.site.framework.interceptor;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import ajob.framework.Log;
import ajob.framework.SystemContext;
import ajob.util.IdUtil;
import ajob.util.IpUtil;

import org.springframework.web.servlet.HandlerInterceptor;

/**
 * 用户登陆校验权限验证器
 * @author cqchen 2018年5月9日14:35:36
 *
 */
public class AuthInterceptor implements HandlerInterceptor {

	@Override
	public boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object handler) throws Exception {
		
		SystemContext context = SystemContext.newInstance();
		context.setChannel("0000");
		context.setClientIp(IpUtil.getRequestIp(request));
		context.setClientVersion("1.0.0");
		context.setServiceVersion(0);
		
		context.setImei(request.getSession().getId().replaceAll("-", ""));
		context.setPlatform("");		//TODO
		context.setReqId(IdUtil.createUuid());
		context.setReqTime(System.currentTimeMillis());
		context.setStartTime(System.currentTimeMillis());
		context.setUa(request.getHeader("User-Agent"));
		context.setServiceName(request.getRequestURI());
		
		context.setUserId(1);		//TODO 先写死ID
		
		String url = request.getRequestURI();
		Log.info("用户请求接入：{}", url);
		
		//校验是否需要登陆，进行登陆状态验证 TODO
		
		//进行访问权限控制 TODO
		
		return true;
	}
}
