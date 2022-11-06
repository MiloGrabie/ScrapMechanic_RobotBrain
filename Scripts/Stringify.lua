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
    for index, joint in ipairs(main.interactable:getBearings()) do
        out_table.joints[index] = {
			index =  index,
            angle = joint.angle,
			localPosition = VectToString(joint.localPosition),
			localRotation = QuatToString(joint.localRotation),
			position = VectToString(joint.worldPosition),
        }
		print("angle", joint.angle)
    end
	return out_table
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