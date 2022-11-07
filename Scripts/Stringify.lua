function stringify(main)
	shape = main.interactable.shape
	body = main.interactable:getBody()
	ang = shape:getWorldRotation()
	pos = body:getWorldPosition()
	vel = shape:getVelocity()
	mass = body:getMass()

	out_table = {
		ang = VectToString(ang),
		pos = VectToString(pos),	
		vel = VectToString(vel),
		mass = mass
	}
    
    out_table.joints = {}

    for index, joint in ipairs(body:getJoints()) do
--         joint = body:getJoints()[1]
        first_joint = joint
        joint_dico = {}
        pointer = joint_dico
        while true do
            sub_dico = {}
            sub_dico[joint.id] = jointToJsonTable(joint)
            pointer.joints = sub_dico
            pointer = sub_dico[joint.id]
            if joint.shapeB == nil then break end
            if joint == nil then break end
            joint = joint.shapeB.body:getJoints()[1]
        end
--         print(joint_dico.joints)
--         print(first_joint.id)
        out_table.joints[first_joint.id] = joint_dico.joints[first_joint.id]
--         print(out_table)
    end
	return out_table
end

function jointToJsonTable(joint)
    return {
        index =  joint.id,
        angle = joint.angle,
        localPosition = VectToString(joint.localPosition),
        localRotation = QuatToString(joint.localRotation),
        position = VectToString(joint.worldPosition),
        xAxis = VectToString(joint.xAxis),
        yAxis = VectToString(joint.yAxis),
        zAxis = VectToString(joint.zAxis),
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