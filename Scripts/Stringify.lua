function stringify(main, body, angle, ang, pos, vel, mass)
	out_table = {
		ang = {
			x = ang.x,
			y = ang.y,
			z = ang.z,
			w = ang.w
		},
		pos = {
			x = pos.x,
			y = pos.y,
			z = pos.z,
		},		
		vel = {
			x = vel.x,
			y = vel.y,
			z = vel.z,
		},
		mass = mass
	}
    
    out_table.joints = {}
    for index, value in ipairs(main.interactable:getBearings()) do
        out_table.joints[index] = {
			index =  index,
            angle = value.angle
        }
    end

	return out_table
end
