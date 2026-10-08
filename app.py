from flask import Flask,render_template,request
import parking

app=Flask(__name__)

@app.route("/",methods=["GET","POST"])
def index():
    form={"type":"Standard","x":"","y":""}
    result=None
    message=""
    allocated=False
    vehicle=None
    if request.method=="POST":
        action=request.form["action"]
        if action=="reset":
            parking.reset()
            message="Parking lot reset."
        else:
            form["type"]=request.form["type"]
            try:
                form["x"]=int(request.form["x"])
                form["y"]=int(request.form["y"])
            except ValueError:
                message="Click the road to set the vehicle position."
            else:
                if not parking.is_road(form["x"],form["y"]):
                    message="Click a road cell to set the vehicle position."
                else:
                    vehicle=(form["x"],form["y"])
                    result=parking.find_best_slot(form["x"],form["y"],form["type"])
                    if result is None:
                        message="No available compatible slot."
                    elif action=="allocate":
                        parking.allocate(result["best"]["id"])
                        allocated=True
                    elif action=="cancel":
                        message="Allocation cancelled. Slot "+result["best"]["id"]+" stays available."
                        result=None
    return render_template("index.html",slots=parking.slots,form=form,
                           result=result,message=message,allocated=allocated,vehicle=vehicle)

if __name__=="__main__":
    app.run(debug=False)
