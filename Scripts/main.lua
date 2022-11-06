dofile("LuaPython.lua")

local A = class(function(A)
    function A.__init__(self)
        print("hello world")
    end
    function A.print_msg(self)
        print("test")
    end
    return A
end, {})

function run(msg)
    local a = A()
    a.print_msg()
end