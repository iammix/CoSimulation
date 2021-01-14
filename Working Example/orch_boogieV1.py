from pyfmi import load_fmu

model = load_fmu('BoogiefmuV1.fmu')


duration_reference = model.get_model_variables()["duration"].value_reference
model.set_real([duration_reference, ], [10.0, ])
res = model.simulate()


print(res["duration"])

