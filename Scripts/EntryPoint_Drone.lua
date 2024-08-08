main_class = class( nil )
main_class.maxChildCount = -1
main_class.maxParentCount = -1
main_class.connectionInput = sm.interactable.connectionType.logic
main_class.connectionOutput = sm.interactable.connectionType.bearing + sm.interactable.connectionType.logic -- none, logic, power, bearing, seated, piston, any
main_class.camera_data = 0

dofile("utils.lua")
dofile("Stringify.lua")
dofile("ReadInput.lua")

print("\n\n\n\n=================== RESET ================\n\n\n\n")

camera_data = class(nil)

--[[ client ]]
function main_class.client_onCreate( self )
end
function main_class.client_onRefresh( self ) 
	self:client_onCreate()
		
end

function main_class.client_onUpdate( self, deltaTime )
	-- read(self, deltaTime)
	try {
		function()

			index = index + 1
			if index % 1 ~= 0 then
				return nil
			end

			self.camera_data = sm.camera.getDirection()

			local a = 0.7071
			local b = 0

			sm.localPlayer.setLockedControls(false)
			--print(-self.shape.right)
			local rot = self.interactable.shape.worldRotation
			sm.localPlayer.setDirection(self.interactable.shape:getAt())

		end,
        catch {
            function(error)
                print('caught error: ' .. error)
            end
        }
	}
end

--[[ server ]]
function main_class.server_onCreate( self )
end
function main_class.server_onRefresh( self )
	self:server_onCreate()
end

function main_class.server_onFixedUpdate( self, deltaTime )
	-- read(self, deltaTime)
	try {
		function()
			read(self, deltaTime)
		end,
        catch {
            function(error)
                print('caught error: ' .. error)
            end
        }
	}
end

index = 0
input = nil
function read(self, deltaTime)

	index = index + 1
	if index % 1 ~= 0 then
		return nil
	end

    print("loop")
	--print(self.interactable:getConnectionInputType())
	shape = self.interactable.shape
	body = self.interactable:getBody()
-- 	print(shape.localPosition)
	input = read_input()	
	
	sm.json.save(sm.json.writeJsonString(stringify(self, self.camera_data)), "$MOD_DATA/Scripts/JSON/interface_out.json")

--     print(input.disarm)
	if input.disarm ~= nil and input.disarm == true then
	    for _, joint in ipairs(self.interactable:getBearings()) do
	        sm.joint.setTargetAngle(joint, 0, 1, 1)
	    end
	    return
    end



	if input.destruct ~= nil then
		local destructIndex = input.destruct
		print(destructIndex)
		if destructIndex == body.id then
			print('Destroyed !')
			sm.physics.explode(shape.worldPosition, 7, 2, 6, 25, "PropaneTank - ExplosionSmall")
			sm.body.destroyBody(body)
		end
	end

	if input.setTargetAngle ~= nil then
		for index, joint in ipairs(input.setTargetAngle) do
-- 			print(joint.targetAngle, joint.angularVelocity, joint.maxImpulse)
			for _, local_joint in ipairs(self.interactable:getBearings()) do
			    if (local_joint.id == joint.index) then
			        sm.joint.setTargetAngle(local_joint, joint.targetAngle, joint.angularVelocity, joint.maxImpulse)
                end
			end
		end
	end

    if input.applyTorque ~= nil then
        for index, torque in ipairs(input.applyTorque) do
            print("Applying torque:", torque.torque_vector)
            sm.physics.applyTorque(body, tableToVec3(torque.torque_vector), false)
        end
    end

    if input.applyImpulse ~= nil then
		for index, impulse in ipairs(input.applyImpulse) do
            print("Applying impulse:", impulse.impulse_vector)
			sm.physics.applyImpulse(body, tableToVec3(impulse.impulse_vector), false)
		end
    end

    self.interactable.active = outputs
end