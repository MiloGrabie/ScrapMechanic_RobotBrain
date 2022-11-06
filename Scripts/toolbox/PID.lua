PID = {
    error_prior = 0,
    integral_prior = 0,
    kp = 0.4,
    ki = 0.1,
    kd = 0.01,
    bias = 0
}

function PID:new (o)
    o = o or {}
    setmetatable(o, self)
    self.__index = self    
    self.error_prior = 0,
    self.integral_prior = 0,
    self.kp = 0.4,
    self.ki = 0.1,
    self.kd = 0.01,
    self.bias = 0
end

function onTick(objective, actualValue)	
	error = objective - actualValue
	integral = integral_prior+error
	derivative = error-error_prior
	
	value_out = kp*error+ki*integral+kd*derivative+bias
	
	error_prior = error
	integral_prior = integral
	
	return value_out
end