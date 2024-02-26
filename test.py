mach_brands = {'1': ['АИ-80'], '2': ['АИ-92'], '3': ['АИ-92', 'АИ-95', 'АИ-98']}
brand = 'АИ-92'

opt_mach = []
for mach, brnd in mach_brands.items():
        if brand in brnd:
            opt_mach.append(mach)
            print(opt_mach)

if len(opt_mach) == 1:
      
      