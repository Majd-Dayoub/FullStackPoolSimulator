#include "phylib.h"

// Part 1: Constructor Functions

// Function 1 : Working

phylib_object *phylib_new_still_ball(unsigned char number, phylib_coord *pos)
{
    // Allocate memory for the phylib_object
    phylib_object *obj = (phylib_object *)malloc(sizeof(phylib_object));

    // Check if memory allocation was successful
    if (obj != NULL)
    {
        // Set the type to PHYLIB_STILL_BALL
        obj->type = PHYLIB_STILL_BALL;

        // Transfer information from function parameters
        obj->obj.still_ball.number = number;
        obj->obj.still_ball.pos = *pos;
    }

    // Return a pointer to the phylib_object
    return obj;
}
// Function 2 : Working
phylib_object *phylib_new_rolling_ball(unsigned char number, phylib_coord *pos, phylib_coord *vel, phylib_coord *acc)
{
    // Allocate memory for the new phylib_object
    phylib_object *obj = (phylib_object *)malloc(sizeof(phylib_object));

    if (obj != NULL)
    {
        // Set the type to PHYLIB_ROLLING_BALL
        obj->type = PHYLIB_ROLLING_BALL;

        // Initialize the rolling ball properties
        obj->obj.rolling_ball.number = number;
        obj->obj.rolling_ball.pos = *pos;
        obj->obj.rolling_ball.vel = *vel;
        obj->obj.rolling_ball.acc = *acc;
    }

    return obj;
}
// Function 3 : Working
phylib_object *phylib_new_hole(phylib_coord *pos)
{
    // Allocate memory for a new phylib_object
    phylib_object *obj = (phylib_object *)malloc(sizeof(phylib_object));

    if (obj != NULL)
    {
        // Set the type to PHYLIB_HOLE
        obj->type = PHYLIB_HOLE;

        // Initialize the hole properties
        obj->obj.hole.pos = *pos;
    }

    return obj;
}
// Function 4 : Working
phylib_object *phylib_new_hcushion(double y)
{
    // Allocate memory for a new phylib_object
    phylib_object *obj = (phylib_object *)malloc(sizeof(phylib_object));

    if (obj != NULL)
    {
        // Set the type to PHYLIB_HCUSHION
        obj->type = PHYLIB_HCUSHION;

        // Initialize the horizontal cushion properties
        obj->obj.hcushion.y = y;
    }

    return obj;
}
// Function 5 : Working
phylib_object *phylib_new_vcushion(double x)
{
    // Allocate memory for a new phylib_object
    phylib_object *obj = (phylib_object *)malloc(sizeof(phylib_object));

    if (obj != NULL)
    {
        // Set the type to PHYLIB_VCUSHION
        obj->type = PHYLIB_VCUSHION;

        // Initialize the vertical cushion properties
        obj->obj.vcushion.x = x;
    }

    return obj;
}

// Function 6 : Working
phylib_table *phylib_new_table(void)
{
    // Allocate memory for the table structure
    phylib_table *table = (phylib_table *)malloc(sizeof(phylib_table));

    // Check for memory allocation failure
    if (table == NULL)
    {
        return NULL;
    }

    // Initialize the time variable
    table->time = 0.0;

    // Create and add a horizontal cushion at y=0.0
    table->object[0] = phylib_new_hcushion(0.0);

    // Create and add a horizontal cushion at y=PHYLIB_TABLE_LENGTH
    table->object[1] = phylib_new_hcushion(PHYLIB_TABLE_LENGTH);

    // Create and add a vertical cushion at x=0.0
    table->object[2] = phylib_new_vcushion(0.0);

    // Create and add a vertical cushion at x=PHYLIB_TABLE_WIDTH
    table->object[3] = phylib_new_vcushion(PHYLIB_TABLE_WIDTH);

    // Create and add 6 holes
    table->object[4] = phylib_new_hole(&(phylib_coord){0.0, 0.0});
    table->object[5] = phylib_new_hole(&(phylib_coord){0.0, PHYLIB_TABLE_WIDTH});
    table->object[6] = phylib_new_hole(&(phylib_coord){0.0, PHYLIB_TABLE_LENGTH});
    table->object[7] = phylib_new_hole(&(phylib_coord){PHYLIB_TABLE_WIDTH, 0.0});
    table->object[8] = phylib_new_hole(&(phylib_coord){PHYLIB_TABLE_WIDTH, PHYLIB_TABLE_WIDTH});
    table->object[9] = phylib_new_hole(&(phylib_coord){PHYLIB_TABLE_WIDTH, PHYLIB_TABLE_LENGTH});

    // Set remaining pointers to NULL
    for (int i = 10; i < PHYLIB_MAX_OBJECTS; i++)
    {
        table->object[i] = NULL;
    }

    return table;
}

// Function 1 : Working
void phylib_copy_object(phylib_object **dest, phylib_object **src)
{
    if (src == NULL || *src == NULL)
    {
        *dest = NULL;
    }
    else
    {

        *dest = (phylib_object *)calloc(1, sizeof(phylib_object));

        if (*dest != NULL)
        {
            memcpy(*dest, *src, sizeof(phylib_object)); // copy the contents of the object from src to dest
        }
    }
}

// Function 2 : Working
phylib_table *phylib_copy_table(phylib_table *table)
{
    if (table == NULL)
    {
        // free(table);
        return NULL;
    }
    phylib_table *newTable = calloc(1, sizeof(phylib_table));
    if (newTable == NULL)
    {
        // free(newTable);
        return NULL;
    }

    for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++)
    {
        if (table->object[i] != NULL)
        {
            // Free the existing object in newTable before copying
            // free(newTable->object[i]);
            phylib_copy_object(&newTable->object[i], &table->object[i]);
        }
    }
    newTable->time = table->time;
    return newTable;
}

// Function 3 : Working
void phylib_add_object(phylib_table *table, phylib_object *object)
{
    // Check if either the table or object pointers are NULL
    if (table == NULL || object == NULL)
    {
        return; // Do nothing if either pointer is NULL
    }

    // Iterate over the object array in the table
    for (int i = 0; i < PHYLIB_MAX_OBJECTS; ++i)
    {
        // Check if the current object pointer is NULL
        if (table->object[i] == NULL)
        {
            // Assign the address of the object to the NULL pointer
            table->object[i] = object;
            return; // Exit the function after adding the object
        }
    }
}

// Function 4 : Working
void phylib_free_table(phylib_table *table)
{
    // Check if the table pointer is NULL
    if (table == NULL)
    {
        return; // Do nothing if the pointer is NULL
    }

    // Iterate over the object array in the table
    for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++)
    {
        // Check if the current object pointer is non-NULL
        if (table->object[i] != NULL)
        {
            // Free the memory allocated for the current object
            free(table->object[i]);
            table->object[i] = NULL;
        }
    }

    // Free the memory allocated for the table
    free(table);
}

// Function 5 : Working
phylib_coord phylib_sub(phylib_coord c1, phylib_coord c2)
{
    phylib_coord difference;

    // Calculate the difference between c1 and c2
    difference.x = c1.x - c2.x;
    difference.y = c1.y - c2.y;

    return difference;
}

// Function 6 : Working
double phylib_length(phylib_coord c)
{
    double result = (c.x * c.x) + (c.y * c.y);
    return sqrt(result);
}

// Function 7 phylib_dot_product : Working
double phylib_dot_product(phylib_coord a, phylib_coord b)
{
    return a.x * b.x + a.y * b.y;
}

// Function 8 phylib_distance : Working
double phylib_distance(phylib_object *obj1, phylib_object *obj2)
{
    // Check if obj1 is a PHYLIB_ROLLING_BALL
    if (obj1->type != PHYLIB_ROLLING_BALL)
    {
        return -1.0;
    }

    // Extract coordinates of obj1 (PHYLIB_ROLLING_BALL)
    double x1 = obj1->obj.rolling_ball.pos.x;
    double y1 = obj1->obj.rolling_ball.pos.y;

    // Calculate distance based on the type of obj2
    switch (obj2->type)
    {
    case PHYLIB_ROLLING_BALL:
    case PHYLIB_STILL_BALL:
        // Distance between ball centers minus two radii
        return phylib_length(phylib_sub(obj1->obj.rolling_ball.pos, obj2->obj.still_ball.pos)) - PHYLIB_BALL_DIAMETER;

    case PHYLIB_HOLE:
        // Distance between ball center and hole center minus HOLE_RADIUS
        return phylib_length(phylib_sub(obj1->obj.rolling_ball.pos, obj2->obj.hole.pos)) - PHYLIB_HOLE_RADIUS;

    case PHYLIB_HCUSHION:
        // Distance between ball center and cushion center minus BALL_RADIUS
        return fabs(y1 - obj2->obj.hcushion.y) - PHYLIB_BALL_RADIUS;

    case PHYLIB_VCUSHION:
        // Distance between ball center and cushion center minus BALL_RADIUS
        return fabs(x1 - obj2->obj.vcushion.x) - PHYLIB_BALL_RADIUS;

    default:
        // Return -1.0 for invalid obj2 types
        return -1.0;
    }
}

// Part 3: Dynamic Functions

// Function 1 : Working

void phylib_roll(phylib_object *new, phylib_object *old, double time)
{
    // Check if both new and old are PHYLIB_ROLLING_BALLs
    if (new == NULL || old == NULL || new->type != PHYLIB_ROLLING_BALL || old->type != PHYLIB_ROLLING_BALL)
    {
        return; // Do nothing if not PHYLIB_ROLLING_BALLs
    }

    // Update position using the kinematic equation
    new->obj.rolling_ball.pos.x = old->obj.rolling_ball.pos.x +
                                  (old->obj.rolling_ball.vel.x * time) +
                                  ((0.5 * old->obj.rolling_ball.acc.x) * time * time);

    new->obj.rolling_ball.pos.y = old->obj.rolling_ball.pos.y +
                                  (old->obj.rolling_ball.vel.y * time) +
                                  ((0.5 * old->obj.rolling_ball.acc.y) * time * time);

    // Update velocity using the kinematic equation
    new->obj.rolling_ball.vel.x = old->obj.rolling_ball.vel.x +
                                  (old->obj.rolling_ball.acc.x * time);

    new->obj.rolling_ball.vel.y = old->obj.rolling_ball.vel.y +
                                  (old->obj.rolling_ball.acc.y * time);

    // Check if either velocity changes sign
    if ((old->obj.rolling_ball.vel.x * new->obj.rolling_ball.vel.x) < 0.0 &&
        (old->obj.rolling_ball.vel.y * new->obj.rolling_ball.vel.y) < 0.0)
    {
        // If so, set both velocities and accelerations to zero
        new->obj.rolling_ball.vel.x = 0.0;
        new->obj.rolling_ball.vel.y = 0.0;
        new->obj.rolling_ball.acc.x = 0.0;
        new->obj.rolling_ball.acc.y = 0.0;
    }
    else if ((old->obj.rolling_ball.vel.x * new->obj.rolling_ball.vel.x) < 0.0)
    {
        new->obj.rolling_ball.vel.x = 0.0;
        new->obj.rolling_ball.acc.x = 0.0;
    }
    else if (((old->obj.rolling_ball.vel.y * new->obj.rolling_ball.vel.y) < 0.0))
    {
        new->obj.rolling_ball.vel.y = 0.0;
        new->obj.rolling_ball.acc.y = 0.0;
    }
}

// Function 2 : Working
unsigned char phylib_stopped(phylib_object *object)
{
    // Check if the object is a ROLLING_BALL
    if (object->type == PHYLIB_ROLLING_BALL)
    {

        // Calculate the speed (length of velocity)
        double speed = phylib_length(object->obj.rolling_ball.vel);

        // Check if the speed is less than PHYLIB_VEL_EPSILON
        if (speed < PHYLIB_VEL_EPSILON)
        {
            // Convert the ROLLING_BALL into a STILL_BALL directly
            object->type = PHYLIB_STILL_BALL;

            // Set velocity and acceleration to zero for the still ball
            object->obj.still_ball.pos = object->obj.rolling_ball.pos;
            object->obj.still_ball.number = object->obj.rolling_ball.number;

            // Return 1 to indicate conversion
            return 1;
        }
    }

    // Return 0 if the ball is not stopped or not a ROLLING_BALL
    return 0;
}

// Function 3
void phylib_bounce(phylib_object **a, phylib_object **b)
{
    if (*b == NULL)
    {
        return; // No collision if b is null
    }

    double r_ab_x, r_ab_y, v_rel_x, v_rel_y, r_ab_length, n_x, n_y, v_rel_n, speed_a, speed_b;

    switch ((*b)->type)
    {
    case PHYLIB_HCUSHION:
        (*a)->obj.rolling_ball.vel.y = -(*a)->obj.rolling_ball.vel.y;
        (*a)->obj.rolling_ball.acc.y = -(*a)->obj.rolling_ball.acc.y;
        break;

    case PHYLIB_VCUSHION:
        (*a)->obj.rolling_ball.vel.x = -(*a)->obj.rolling_ball.vel.x;
        (*a)->obj.rolling_ball.acc.x = -(*a)->obj.rolling_ball.acc.x;
        break;

    case PHYLIB_HOLE:
        free(*a);
        *a = NULL;
        break;
    case PHYLIB_STILL_BALL:
        (*b)->obj.rolling_ball.pos = (*b)->obj.still_ball.pos;
        (*b)->obj.rolling_ball.number = (*b)->obj.still_ball.number;
        (*b)->obj.rolling_ball.vel.x = 0.0;
        (*b)->obj.rolling_ball.vel.y = 0.0;
        (*b)->obj.rolling_ball.acc.x = 0.0;
        (*b)->obj.rolling_ball.acc.y = 0.0;
        (*b)->type = PHYLIB_ROLLING_BALL; // "Upgrade" STILL_BALL to ROLLING_BALL then go to next case

    case PHYLIB_ROLLING_BALL:
        // Compute the position of a with respect to b: subtract the position of b from a; call it r_ab
        r_ab_x = (*a)->obj.rolling_ball.pos.x - (*b)->obj.rolling_ball.pos.x;
        r_ab_y = (*a)->obj.rolling_ball.pos.y - (*b)->obj.rolling_ball.pos.y;
        // Compute the relative velocity of a with respect to b: subtract the velocity of b from a;call it v_rel
        v_rel_x = (*a)->obj.rolling_ball.vel.x - (*b)->obj.rolling_ball.vel.x;
        v_rel_y = (*a)->obj.rolling_ball.vel.y - (*b)->obj.rolling_ball.vel.y;
        // Divide the x and y components of r_ab by the length of r_ab; call that a normal vector, n
        r_ab_length = sqrt(r_ab_x * r_ab_x + r_ab_y * r_ab_y);
        n_x = r_ab_x / r_ab_length;
        n_y = r_ab_y / r_ab_length;
        // Calculate the ratio of the relative velocity, v_rel, in the direction of ball a by computing the dot_product of v_rel with respect to n; call that v_rel_n
        v_rel_n = v_rel_x * n_x + v_rel_y * n_y;
        // Update the x velocity of ball a by subtracting v_rel_n multipied by the x component of
        // vector n. Similarly, Update the y velocity of ball a by subtracting v_rel_n multipied by the y component of vector n.
        (*a)->obj.rolling_ball.vel.x -= v_rel_n * n_x;
        (*a)->obj.rolling_ball.vel.y -= v_rel_n * n_y;
        // Update the x and y velocities of ball b by adding the product of v_rel_n and vector n
        (*b)->obj.rolling_ball.vel.x += v_rel_n * n_x;
        (*b)->obj.rolling_ball.vel.y += v_rel_n * n_y;

        // Compute the speed of a and b as the lengths of their velocities.
        speed_a = sqrt(
            (*a)->obj.rolling_ball.vel.x * (*a)->obj.rolling_ball.vel.x +
            (*a)->obj.rolling_ball.vel.y * (*a)->obj.rolling_ball.vel.y);
        speed_b = sqrt(
            (*b)->obj.rolling_ball.vel.x * (*b)->obj.rolling_ball.vel.x +
            (*b)->obj.rolling_ball.vel.y * (*b)->obj.rolling_ball.vel.y);

        // if the speed is greater than PHYLIB_VEL_EPSILON then set the acceleration of the ball to the negative
        // velocity divided by the speed multiplied by PHYLIB_DRAG.
        if (speed_a > PHYLIB_VEL_EPSILON)
        {
            (*a)->obj.rolling_ball.acc.x = -((*a)->obj.rolling_ball.vel.x / speed_a) * PHYLIB_DRAG;
            (*a)->obj.rolling_ball.acc.y = -((*a)->obj.rolling_ball.vel.y / speed_a) * PHYLIB_DRAG;
        }
        if (speed_b > PHYLIB_VEL_EPSILON)
        {
            (*b)->obj.rolling_ball.acc.x = -((*b)->obj.rolling_ball.vel.x / speed_b) * PHYLIB_DRAG;
            (*b)->obj.rolling_ball.acc.y = -((*b)->obj.rolling_ball.vel.y / speed_b) * PHYLIB_DRAG;
        }

        break;
    }
}

unsigned char phylib_rolling(phylib_table *t)
{
    unsigned char rollingBallCount = 0;
    int i;

    for (i = 0; i < PHYLIB_MAX_OBJECTS; i++)
    {
        if (t->object[i] != NULL && t->object[i]->type == PHYLIB_ROLLING_BALL)
        {
            rollingBallCount += 1.0;
        }
    }

    return rollingBallCount;
}
void print_table(phylib_table *table) {
    if (table == NULL) {
        printf("Table is NULL\n");
        return;
    }

    for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++) {
        if (table->object[i] != NULL) {
            printf("Object %d: %s\n", i, phylib_object_string(table->object[i]));
        }
    }
}

phylib_table *phylib_segment(phylib_table *table)
{
    
    if (table == NULL)
    {
        return NULL;
    }

    unsigned char rolling_balls_count = phylib_rolling(table);
    
    if (rolling_balls_count == 0)
    {
        return NULL;
    }

    phylib_table *result_table = phylib_copy_table(table); // make a copy of the table

    double current_time = PHYLIB_SIM_RATE;
    
    while (current_time <= PHYLIB_MAX_TIME)
    {

        for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++)
        {
            if (result_table->object[i] != NULL && result_table->object[i]->type == PHYLIB_ROLLING_BALL)
            {
                // Perform rolling physics for the rolling ball
                phylib_roll(result_table->object[i], table->object[i], current_time);
            }
        }

        for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++)
        {
            if (result_table->object[i] != NULL && result_table->object[i]->type == PHYLIB_ROLLING_BALL)
            {
                for (int j = 0; j < PHYLIB_MAX_OBJECTS; j++)
                {
                    if (result_table->object[j] != NULL && i != j)
                    {
                        if (phylib_distance(result_table->object[i], result_table->object[j]) < 0.0)
                        {
                            phylib_bounce(&(result_table->object[i]), &(result_table->object[j]));
                            result_table->time += current_time;
                            return result_table;
                        }
                    }
                    
                    if (phylib_stopped(result_table->object[i]))
                    {
                        result_table->time += current_time;
                        return result_table;
                    }
                }
            }
        }

        current_time += PHYLIB_SIM_RATE;
    }

    return NULL;
}



// ADDED FUNCTION FOR A2
char *phylib_object_string(phylib_object *object)
{
    static char string[80];
    if (object == NULL)
    {
        snprintf(string, 80, "NULL;");
        return string;
    }
    switch (object->type)
    {
    case PHYLIB_STILL_BALL:
        snprintf(string, 80,
                 "STILL_BALL (%d,%6.1lf,%6.1lf)",
                 object->obj.still_ball.number,
                 object->obj.still_ball.pos.x,
                 object->obj.still_ball.pos.y);
        break;
    case PHYLIB_ROLLING_BALL:
        snprintf(string, 80,
                 "ROLLING_BALL (%d,%6.1lf,%6.1lf,%6.1lf,%6.1lf,%6.1lf,%6.1lf)",
                 object->obj.rolling_ball.number,
                 object->obj.rolling_ball.pos.x,
                 object->obj.rolling_ball.pos.y,
                 object->obj.rolling_ball.vel.x,
                 object->obj.rolling_ball.vel.y,
                 object->obj.rolling_ball.acc.x,
                 object->obj.rolling_ball.acc.y);
        break;
    case PHYLIB_HOLE:
        snprintf(string, 80,
                 "HOLE (%6.1lf,%6.1lf)",
                 object->obj.hole.pos.x,
                 object->obj.hole.pos.y);
        break;
    case PHYLIB_HCUSHION:
        snprintf(string, 80,
                 "HCUSHION (%6.1lf)",
                 object->obj.hcushion.y);
        break;
    case PHYLIB_VCUSHION:
        snprintf(string, 80,
                 "VCUSHION (%6.1lf)",
                 object->obj.vcushion.x);
        break;
    }
    return string;
}
