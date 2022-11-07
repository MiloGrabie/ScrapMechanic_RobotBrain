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
        if joint:getShapeA().id ~= shape.id then
            out_table.joints[joint.id] = {
                index =  joint.id,
                angle = joint.angle,
                localPosition = VectToString(joint.localPosition),
                localRotation = QuatToString(joint.localRotation),
                position = VectToString(joint.worldPosition),
                xAxis = VectToString(joint.xAxis),
                yAxis = VectToString(joint.yAxis),
                zAxis = VectToString(joint.zAxis),
            }
            out_table.joints[joint.id].joints = {}
            for indexB, jointB in ipairs(joint.shapeB.body:getJoints()) do
                out_table.joints[joint.id].joints[jointB.id] = {
                    indexB =  jointB.id,
                    angle = jointB.angle,
                    localPosition = VectToString(jointB.localPosition),
                    localRotation = QuatToString(jointB.localRotation),
                    position = VectToString(jointB.worldPosition),
                    xAxis = VectToString(jointB.xAxis),
                    yAxis = VectToString(jointB.yAxis),
                    zAxis = VectToString(jointB.zAxis),
                }
                out_table.joints[joint.id].joints[jointB.id].joints = {}
                for indexC, jointC in ipairs(jointB.shapeB.body:getJoints()) do
                    out_table.joints[joint.id].joints[jointB.id].joints[jointC.id] = {
                        indexB =  jointC.id,
                        angle = jointC.angle,
                        localPosition = VectToString(jointC.localPosition),
                        localRotation = QuatToString(jointC.localRotation),
                        position = VectToString(jointC.worldPosition),
                        xAxis = VectToString(jointC.xAxis),
                        yAxis = VectToString(jointC.yAxis),
                        zAxis = VectToString(jointC.zAxis),
                    }
                end
            end
        end
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