add_rules("mode.debug", "mode.release")

set_languages("cxx11")
add_requires("boost", "pthread")
add_packages("boost", "pthread")
add_syslinks("pthread")

if is_mode("debug") then
    add_defines("DEBUG")
end

includes("read_data")
includes("crossover")