package ajob.site.framework;

import javax.servlet.http.HttpServletRequest;

import ajob.framework.Log;
import ajob.framework.service.ResponseData;

import org.springframework.web.bind.annotation.ControllerAdvice;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.ResponseBody;
import org.springframework.web.method.annotation.MethodArgumentTypeMismatchException;

/**
 * MVC映射异常的处理方法
 * @author cqchen 2018年5月9日15:32:56
 *
 */
@ControllerAdvice
public class SiteMvcExceptionHandler {

	/**
	 * 参数类型转换有误异常
	 * @param request
	 * @param e
	 * @return
	 */
	@ResponseBody
	@ExceptionHandler(MethodArgumentTypeMismatchException.class)  
	public String argumentTypeMismatchException(HttpServletRequest request, MethodArgumentTypeMismatchException e) {
		Log.error("MVC映射参数转换异常：url={}, paramName={}, paramValue={}", request.getQueryString(), e.getName(), e.getValue());
		return ResponseData.createFail("参数类型有误：" + e.getName() + "=" + e.getValue()).toJson();
	}
}
