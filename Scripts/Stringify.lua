function stringify(main)
	shape = main.interactable.shape
	body = main.interactable:getBody()
	rot = shape:getWorldRotation()
	pos = body:getWorldPosition()
	vel = shape:getVelocity()
    print(vel)
	mass = body:getMass()
-- 	print(shape.up)

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
        index = body.id
	}
    
    out_table.joints = {}

    for index, joint in ipairs(body:getJoints()) do
        print(joint.type)
        if joint.type == 'bearing' then

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
        end
--         print(joint_dico.joints)
--         print(first_joint.id)
        out_table.joints[first_joint.id] = joint_dico.joints[first_joint.id]
--         print(out_table)
    end
	return out_table
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