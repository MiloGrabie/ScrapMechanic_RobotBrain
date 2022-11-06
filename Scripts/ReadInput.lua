dofile("utils.lua")

function read_input()
	-- try {
    --     function()
    input_path = "$MOD_DATA/Scripts/JSON/interface_in.json"
    data = sm.json.open(input_path)
    return data
    --     end,
    --     catch {
    --         function(error)
    --             print('caught error: ' .. error)
    --         end
    --     }
    -- }
end