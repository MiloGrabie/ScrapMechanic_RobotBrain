function stringify(main)
	shape = main.interactable.shape
	body = main.interactable:getBody()
	rot = shape:getWorldRotation()
	pos = body:getWorldPosition()
	vel = shape:getVelocity()
    print(vel)
	mass = body:getMass()

--     print(body.centerOfMassPosition)
	out_table = {
		rot = QuatToString(rot),
		pos = VectToString(pos),
-- 		dir = VectToString(rot * sm.vec3.new(0,0,1)),
		dir = VectToString(-shape.right),
		vel = VectToString(vel),
		mass_center = VectToString(body.centerOfMassPosition),
		mass = mass,
		shape = shapeToString(shape),
        index = body.id,
        at = VectToString(shape.at)
	}

    out_table.joints = {}

    local connectedInteractables = main.interactable:getChildren(sm.interactable.connectionType.bearing)

    for index, joint in ipairs(body:getJoints()) do
        -- print(joint.type)
        if joint.type == 'bearing' then

            local is_connected = false

            for _, connectedInteractable in ipairs(connectedInteractables) do
                if joint.id == connectedInteractable.id then
                        is_connected = true
                    break
                end
            end

            if is_connected == false then
                goto continue
            end
                

    --         joint = body:getJoints()[1]
            first_joint = joint
            joint_dico = {}
            pointer = joint_dico
            while true do
                if joint == nil then break end
                sub_dico = {}
                sub_dico[joint.id] = jointToJsonTable(joint)
                pointer.joints = sub_dico
                pointer = sub_dico[joint.id]
                if joint.shapeB ~= nil then
                    joint = joint.shapeB.body:getJoints()[1]
                else
                    joint = nil
                end
            end


            ::continue::
        end
--         print(joint_dico.joints)
--         print(first_joint.id)
        out_table.joints[first_joint.id] = joint_dico.joints[first_joint.id]
--         print(out_table)
    end

    -- out_table.raycasts = perform_raycasts()
    -- print(out_table)

	return out_table
end

function perform_raycasts()
    
    local raycasts = {}
    
    local thetaMin = math.pi / 4 -- minimum theta (in radians)
    local thetaMax = math.pi / 2 -- maximum theta (in radians)
    local phiMin = 0 -- minimum phi (in radians)
    local phiMax = math.pi / 2 -- maximum phi (in radians)
    local points = createSphereWindow(shape:getWorldPosition(), 500, 50, 50, thetaMin, thetaMax, phiMin, phiMax)
    -- local points = generateSpherePoints(800, shape:getWorldPosition(), 500)
    -- print(points)

    local count = 0
    local pt_count = 0
    -- print(circlePoints)
    for _, coords in pairs(points) do
        vector = sm.vec3.new(coords.x, coords.y, coords.z)
        -- valid, distance = sm.physics.distanceRaycast(shape:getWorldPosition(), vector)
        valid, raycast = sm.physics.raycast(shape:getWorldPosition(), vector, body)
        pt_count = pt_count + 1
        -- print(raycast)
        if valid then
            count = count + 1
            -- print(shape:getWorldPosition() - raycast.pointWorld)
            -- raycast = shape:getWorldPosition() + (vector * distance)
            -- table.insert(raycasts, VectToString(raycast))
            table.insert(raycasts, VectToString(shape:getWorldPosition() - raycast.pointWorld))
        end
        table.insert(raycasts, VectToString(coords))
    end
    print(count, pt_count)

    return raycasts
end

function jointToJsonTable(joint)
--     print(sm.joint.getWorldPosition(joint))
--     print(joint:getWorldPosition())
--     print(joint:getWorldRotation())
--     print(joint.localRotation * sm.vec3.new(0,0,1))
    jointJson = {
        index =  joint.id,
        angle = joint.angle,
        localPosition = VectToString(joint.localPosition),
        localRotation = QuatToString(joint.localRotation),
        position = VectToString(joint:getWorldPosition()),
        rotation = QuatToString(joint:getWorldRotation()),
        direction = VectToString(joint.localRotation * sm.vec3.new(0,0,1)),
        xAxis = VectToString(joint.xAxis),
        yAxis = VectToString(joint.yAxis),
        zAxis = VectToString(joint.zAxis),
    }
--     print(joint.id)
--     print(joint.localRotation * sm.vec3.new(0,0,1))

    if joint.shapeB ~= nil then
        if joint.shapeB.material == "Wood" then
--             print(joint.shapeB.body.centerOfMassPosition)
--             print(joint.shapeB.body.worldPosition)
        end
        jointJson.shapeB = shapeToString(joint.shapeB)
    end
    return jointJson
end

function shapeToString(shape)
   return {
        pos = VectToString(shape.body.centerOfMassPosition),
        rot = QuatToString(shape.worldRotation),
        at = VectToString(shape.at),
        up = VectToString(shape.up),
    }
end

function QuatToString(quaternion)
	return {
		x = quaternion.x,
		y = quaternion.y,
		z = quaternion.z,
		w = quaternion.w
	}
end

function VectToString(vect)
	return {
		x = vect.x,
		y = vect.y,
		z = vect.z,
	}
end