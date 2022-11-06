main_class = class( nil )
main_class.maxChildCount = -1
main_class.maxParentCount = -1
main_class.connectionInput = sm.interactable.connectionType.logic
main_class.connectionOutput = sm.interactable.connectionType.bearing + sm.interactable.connectionType.logic -- none, logic, power, bearing, seated, piston, any
-- main_class.connectionOutput = sm.interactable.connectionType.bearing + sm.interactable.connectionType.power  -- none, logic, power, bearing, seated, piston, any
main_class.colorNormal = sm.color.new(0xdf7000ff)
main_class.colorHighlight = sm.color.new(0xef8010ff)
--main_class.poseWeightCount = 1
dofile("bearing_manager.lua")
dofile("pid.lua")
dofile("keys.lua")

print("\n\n\n\n=================== RESET ================\n\n\n\n")


--[[ client ]]
function main_class.client_onCreate( self )
end
function main_class.client_onRefresh( self ) 
	self:client_onCreate()
end

function main_class.client_onUpdate( self, deltaTime )
end

--[[ server ]]
function main_class.server_onCreate( self )
end
function main_class.server_onRefresh( self )
	self:server_onCreate()
end

thrust=0
index=0
state=true
stop=false
height_prior=0

function main_class.server_onFixedUpdate( self, deltaTime )
	main(self, deltaTime)	
end

function main(self, deltaTime)
	try {
		function()
			index = index + 1

			if index <= 100 then return end

			if index % 1 ~= 0 then
				return nil
			end

			-- if index >= 100 then return end
			
			-- print("testoux")

			-- print(self.interactable.shape:getWorldRotation())
			shape = self.interactable.shape
			body = self.interactable:getBody()
			ang = shape:getWorldRotation()
			pos = body:getWorldPosition()
			vel = shape:getVelocity()
			masse = body:getMass()
			hauteur = pos['z']
			local output = false

			-- local angle = 180
			local actualValue = pos['z']
			-- local deltaLimite = 0.1
			local objectif = 34
			-- local endpoint = math.max(objectif - actualValue, deltaLimite)
			-- local input = actualV	alue
			local max_delta = 1
			local input = vel['z']
			-- print("Objectif :", objectif, "Input :", input)
			print(input)
			if hauteur >= objectif then stop=true end
			
			thrust = 200

			if stop == true then
				-- if input <= 0.0001 then input = 0 end

				print("Input :", input)
				thrust_delta = onTick(0, input) * masse
				thrust = thrust_delta
				print("PID thrust :", thrust)
			end

			-- print("Thrust :", thrust)
			max_impulse = 500
			min_impulse = -500
			if (thrust >= max_impulse) then thrust = max_impulse end
			if (thrust <= min_impulse) then thrust = min_impulse end
			
			-- print(ang)
			-- up_side = self.interactable.shape:getUp():normalize()
			-- print("up_side :", up_side)
			-- -- glob_vec = sm.vec3.new(ang['x'], ang['y'], ang['z']) - sm.vec3.new(0, thrust, 0)
			-- print(sm.shape.getXAxis(shape))
			-- force = 100
			-- glob_vec = sm.vec3.new(force, force, force) *  sm.vec3.new(ang['x'], ang['y'], ang['z'])
			-- print("glob_vec :  ", glob_vec)

			-- self.interactable.shape:destroyShape()

			-- thrust = 0
			sm.physics.applyImpulse(self.shape, sm.vec3.new(0, 0, thrust), true)
			-- bearing:setMotorVelocity(angle_speed, 10)

			if read_key() ~= "None" then
				
			end

			print("Hauteur : ".. pos['z'], "Thrust :", thrust)
			-- print("endpoint : " .. endpoint, "input : ".. input)
			-- print("output : " .. angle_speed, tostring(output))
			print("==================================================================================")
			-- print("output : " .. tostring(output))
			height_prior = hauteur

			self.interactable.active = output
		end,

		catch {
			function(error)
				print('caught error: ' .. error)
			end
		}
	}
end

function to_deg(value)
	return value  * ( 180 / 3.14159)
end

function to_rad(value)
	return value * (3.14159 / 180)
end

function catch(what)
	return what[1]
end

function try(what)
	status, result = pcall(what[1])
	if not status then
		what[2](result)
	end
	return result
end
