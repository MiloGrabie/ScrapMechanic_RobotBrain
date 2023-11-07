

function try(what)
	status, result = pcall(what[1])
	if not status then
		what[2](result)
	end
	return result
end

function catch(what)
	return what[1]
end

function tableToVec3(vec)
	return sm.vec3.new(vec[1], vec[2], vec[3])
end