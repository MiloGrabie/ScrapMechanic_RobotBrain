

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

-- Function to create a list of vectors that form a portion of a sphere or the full sphere if no window is specified
-- centerX, centerY, centerZ is the center of the sphere
-- radius is the radius of the sphere
-- thetaMin, thetaMax are the minimum and maximum polar angles (in radians)
-- phiMin, phiMax are the minimum and maximum azimuthal angles (in radians)
-- numPointsTheta, numPointsPhi are the number of points in the theta and phi directions
function createSphereWindow(point, radius, numPointsTheta, numPointsPhi, thetaMin, thetaMax, phiMin, phiMax)
    local spherePoints = {}
    local pi = math.pi
    -- If no window is specified, use the full range of the sphere
    thetaMin = thetaMin or 0
    thetaMax = thetaMax or pi
    phiMin = phiMin or 0
    phiMax = phiMax or 2 * pi

	local centerX = point.x
	local centerY = point.y
	local centerZ = point.z

    local thetaStep = (thetaMax - thetaMin) / (numPointsTheta - 1)
    local phiStep = (phiMax - phiMin) / (numPointsPhi - 1)

    for i = 0, numPointsTheta - 1 do
        local theta = thetaMin + i * thetaStep
        for j = 0, numPointsPhi - 1 do
            local phi = phiMin + j * phiStep
            local x = centerX + radius * math.sin(theta) * math.cos(phi)
            local y = centerY + radius * math.sin(theta) * math.sin(phi)
            local z = centerZ + radius * math.cos(theta)
            table.insert(spherePoints, {x = x, y = y, z = z})
        end
    end

    return spherePoints
end

function generateSpherePoints(radius, origin, numPoints)
    -- Initialize the table to hold the points
    local points = {}
    local pi = math.pi
    local dphi = pi * (3 - math.sqrt(5)) -- Approximation to the golden angle in radians

    for i = 1, numPoints do
        -- y goes from -1.5 to 1.5 to ensure points are spread evenly from top to bottom
        local y = 1 - (i / (numPoints + 1)) * 2 
        local radiusAtY = math.sqrt(1 - y*y) -- Radius at y

        local phi = i * dphi
        local x = math.cos(phi) * radiusAtY
        local z = math.sin(phi) * radiusAtY

        -- Convert local sphere coordinates to global coordinates
        local globalX = origin.x + radius * x
        local globalY = origin.y + radius * y
        local globalZ = origin.z + radius * z

        -- Add the point to the points table
        table.insert(points, {x = globalX, y = globalY, z = globalZ})
    end

    return points
end



-- Function to create a list of vectors that form a circle
-- centerX, centerY is the center of the circle
-- radius is the radius of the circle
-- numPoints is the number of points on the circle
function createCircle(centerX, centerY, radius, numPoints)
    local circlePoints = {}
    local angleStep = (2 * math.pi) / numPoints

    for i = 1, numPoints do
        local angle = angleStep * (i - 1)
        local x = centerX + radius * math.cos(angle)
        local y = centerY + radius * math.sin(angle)
        table.insert(circlePoints, {x = x, y = y})
    end

    return circlePoints
end

-- -- Example usage:
-- local centerX = 0 -- x coordinate of the sphere's center
-- local centerY = 0 -- y coordinate of the sphere's center
-- local centerZ = 0 -- z coordinate of the sphere's center
-- local radius = 50 -- radius of the sphere
-- local thetaMin = math.pi / 4 -- minimum theta (in radians)
-- local thetaMax = math.pi / 2 -- maximum theta (in radians)
-- local phiMin = 0 -- minimum phi (in radians)
-- local phiMax = math.pi / 2 -- maximum phi (in radians)
-- local numPointsTheta = 10 -- number of points in theta direction within the window
-- local numPointsPhi = 20 -- number of points in phi direction within the window

-- local sphereWindow = createSphereWindow(centerX, centerY, centerZ, radius, thetaMin, thetaMax, phiMin, phiMax, numPointsTheta, numPointsPhi)

-- -- To print the list of vectors
-- for i, point in ipairs(sphereWindow) do
--     print(string.format("Point %d: (%f, %f, %f)", i, point.x, point.y, point.z))
-- end
