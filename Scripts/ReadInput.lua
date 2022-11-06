dofile("utils.lua")

function read_input()
	-- try {
    --     function()
    input_path = "$MOD_DATA/Scripts/JSON/interface_in.json"
    -- input_path = "C:/Users/Milo/AppData/Roaming/Axolot Games/Scrap Mechanic/User/User_76561198130980987/Mods/Robot_Brain/Scripts/JSON/interface_in.json"
    -- print(sm.json.fileExists(input_path))
    data = sm.json.open(input_path)
    -- input = sm.json.parseJsonString("{\"ang\":{\"w\":0.6654057502746582,\"x\":0.6444915533065796,\"y\":0.2715028822422028,\"z\":0.2610595822334290},\"bearings\":[[2.283187627792358]],\"mass\":85.93750,\"pos\":{\"x\":8.736407279968262,\"y\":1.153214454650879,\"z\":-0.6708719730377197},\"vel\":{\"x\":0.0,\"y\":0.0,\"z\":0.0}}\n")
    -- input = sm.json.parseJsonString("$MOD_DATA/JSON/interface_in.json")
    return data
    --     end,
    --     catch {
    --         function(error)
    --             print('caught error: ' .. error)
    --         end
    --     }
    -- }
end