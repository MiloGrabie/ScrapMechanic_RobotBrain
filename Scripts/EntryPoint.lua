main_class = class( nil )
main_class.maxChildCount = -1
main_class.maxParentCount = -1
main_class.connectionInput = sm.interactable.connectionType.logic
main_class.connectionOutput = sm.interactable.connectionType.bearing + sm.interactable.connectionType.logic -- none, logic, power, bearing, seated, piston, any
-- main_class.connectionOutput = sm.interactable.connectionType.bearing + sm.interactable.connectionType.power  -- none, logic, power, bearing, seated, piston, any
-- main_class.colorNormal = sm.color.new(0xdf7000ff)
-- main_class.colorHighlight = sm.color.new(0xef8010ff)
--main_class.poseWeightCount = 1
-- dofile("bearing_manager.lua")
dofile("toolbox/PID.lua")
-- dofile("keys.lua")
dofile("main.lua")

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
	file = io.open ("temp.lua", "r")
	main(self, deltaTime)
end

function main(self, deltaTime)
	-- run("msg")
end
