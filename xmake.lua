add_rules("mode.release")
-- add_rules("mode.debug")

set_languages("cxx11")

if is_mode("debug") then
    add_defines("DEBUG")
end

includes("read_data")
includes("crossover")