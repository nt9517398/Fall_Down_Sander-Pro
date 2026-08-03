INSERT INTO downfall_table
("barcode", "Description", "Documentation", "ClassA",
 "construction", "face", "grade", "grader",
 "length", "product", "rating", "run_number",
 "shift", "thickness", "width", "t_stamp")
VALUES
(:barcode, :description, :documentation, :classa,
 :construction, :face, :grade, :grader,
 :length, :product, :rating, :run_number,
 :shift, :thickness, :width, CURRENT_TIMESTAMP);
