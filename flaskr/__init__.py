from flask import Flask, jsonify, request, abort
from models import setup_db, Plant
from flask_cors import CORS


#######################################

# Define the create_app function
def create_app(test_config=None):
    # Create and configure the app
    # Include the first parameter: Here, __name__is the name of the current Python module.
    app = Flask(__name__, instance_relative_config=True)
    setup_db(app)
    # for specific allowance  use below
    #CORS(app, resources={r"*/api/*" : {origins: '*'}})
    # adding flask-cors you have to init it with app
    CORS(app)

    # this basically allows for after request trigger
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Headers', 'GET, POST, PATCH, DELETE, OPTIONS')
        return response
    
    # these are the error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False, 
            "error": 404,
            "message": "Not found"
            }), 404
    
    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
        "success": False, 
        "error": 422,
        "message": "unprocessable"
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
        "success": False, 
        "error": 400,
        "message": "bad request"
        }), 400
        
    @app.errorhandler(405)
    def not_found(error):
        return jsonify({
        "success": False, 
        "error": 405,
        "message": "method not allowed"
        }), 405
  
 ## ______________________ ##

 
    @app.route('/')
    def hello_world():
        return 'Welcome to flask test api!'
    
        #@cross_origin
    @app.route('/test')
    def hello_test():
        return jsonify({'message':'HELLO, TEST!'})

    @app.route('/hello')
    def get_greeting():
        return jsonify({'message':'Hello, World!'})
    
    @app.route('/entrees/<int:entree_id>')
    def retrieve_entree(entree_id):
        return 'Entree %d' % entree_id
    
    # @app.route('/entrees', methods=['GET'])
    # def get_entrees():
    #     page = request.args.get('page', 1, type=int)

    ### starting real tests here
    @app.route('/plants', methods=['GET', 'POST'])
    def get_plants():
        page = request.args.get('page', 1, type=int) #this is for pagination purpose 
        start = (page - 1) * 10 # state the start
        end = start + 10 # state the end
        plants = Plant.query.all()
        formatted_plants = [plant.format() for plant in plants]
        return jsonify({
            'success': True,
            # this is how you normally do it
            # 'plants': formatted_plants,
            # but to paginate you use the below approach 
            'plants': formatted_plants[start:end],
            'total_plants': len(formatted_plants)
        })

    # this is to get a specific plant by using id as the query parameter
    @app.route('/plants/<int:plant_id>')
    def get_specific_plant(plant_id):
        plant = Plant.query.filter(Plant.id==plant_id).one_or_none()
        if plant is None:
            abort(404)
        else:  
            formatted_plant =  plant.format()
            return jsonify({
                'success': True,
                'plant': formatted_plant,
                'total_fetched': len([formatted_plant])
            })

    # Return the app instance
    return app