add_rules("mode.release", "mode.debug")

if is_mode("debug") then
    add_defines("DEBUG")
end

includes("read_data")
-- includes("crossover")