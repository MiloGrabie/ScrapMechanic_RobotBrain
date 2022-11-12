main_class = class( nil )
main_class.maxChildCount = -1
main_class.maxParentCount = -1
main_class.connectionInput = sm.interactable.connectionType.logic
main_class.connectionOutput = sm.interactable.connectionType.bearing + sm.interactable.connectionType.logic -- none, logic, power, bearing, seated, piston, any

dofile("utils.lua")
dofile("Stringify.lua")
dofile("ReadInput.lua")

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
	shape = self.interactable.shape
	body = self.interactable:getBody()
-- 	print(shape.localPosition)
	input = read_input()
	
	sm.json.save(sm.json.writeJsonString(stringify(self)), "$MOD_DATA/Scripts/JSON/interface_out.json")

--     print(input.disarm)
	if input.disarm ~= nil and input.disarm == true then
	    for _, joint in ipairs(self.interactable:getBearings()) do
	        sm.joint.setTargetAngle(joint, 0, 1, 1)
	    end
	    return
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
end