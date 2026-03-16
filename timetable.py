from flask import jsonify, redirect
from db import query_db

def timetable_routes(app):

    # @app.route("/generate/v1/<int:semester>")
    # def generate_timetable_v1(semester):
    #     department = "BSc IT"
    #     days = ["Day1", "Day2", "Day3", "Day4", "Day5"]

    #     query_db(
    #         "DELETE FROM timetable WHERE department=? AND semester=?",
    #         (department, semester)
    #     )

    #     subjects = query_db("""
    #         SELECT subject_name, subject_type, hours_per_week
    #         FROM subjects WHERE department=? AND semester=?
    #     """, (department, semester))

    #     period, day = 1, 0
    #     for subject, s_type, hours in subjects:
    #         repeat = 2 if s_type == "lab" else int(hours)
    #         for _ in range(repeat):
    #             query_db(
    #                 "INSERT INTO timetable VALUES (NULL,            ?,?,?,?,?)",
    #                 (department, semester, days[day], period, subject)
    #             )
    #             period += 1
    #             if period > 5:
    #                 period, day = 1, day + 1

    #     return redirect("/student")
    
    # @app.route("/generate/old/<int:semester>/<string:department>")
    # def generate_timetable(semester, department):
    #     print("generate_timetable - ENTRY")
    #     # department = "BSc IT"
    #     days = ["Day-1", "Day-2", "Day-3", "Day-4", "Day-5"]
    #     max_periods = 5

    #     # Clear old timetable
    #     print("Clear old timetable - ENTRY")
    #     query_db(
    #         "DELETE FROM timetable WHERE department=? AND semester=?",
    #         (department, semester)
    #     )

    #     # Fetch subjects
    #     subjects = query_db("""
    #         SELECT subject_id, subject_type, hours_per_week
    #         FROM subjects
    #         WHERE department=? AND semester=?
    #     """, (department, semester))

    #     # Timetable structure
    #     timetable = {
    #         day: {p: None for p in range(1, max_periods + 1)}
    #         for day in days
    #     }

    #     # Separate labs and theory
    #     labs = []
    #     theory = []

    #     for name, s_type, hours in subjects:
    #         if s_type.lower() == "lab":
    #             labs.append((name, 2))  # lab = 2 periods
    #         else:
    #             theory.append((name, int(hours)))

    #     print("PRIOR TO ALL STEPS - ENTRY")
        
    #     # -------------------------------
    #     # Step 1: Place LABS
    #     # -------------------------------
    #     day_index = 0
    #     for lab, duration in labs:
    #         placed = False
    #         while not placed and day_index < len(days):
    #             day = days[day_index]
    #             for p in range(1, max_periods):
    #                 if timetable[day][p] is None and timetable[day][p+1] is None:
    #                     timetable[day][p] = lab
    #                     timetable[day][p+1] = lab
    #                     placed = True
    #                     break
    #             day_index += 1

    #     # -------------------------------
    #     # Step 2: Place THEORY subjects
    #     # -------------------------------
    #     # for subject, hours in theory:
    #     #     day_pointer = 0
    #     #     while hours > 0 and day_pointer < len(days):
    #     #         day = days[day_pointer]

    #     #         # Avoid repeating same subject on same day
    #     #         if subject in timetable[day].values():
    #     #             day_pointer += 1
    #     #             continue

    #     #         for p in range(1, max_periods + 1):
    #     #             if timetable[day][p] is None:
    #     #                 timetable[day][p] = subject
    #     #                 hours -= 1
    #     #                 break

    #     #         day_pointer += 1
        
    #     print("STEP1 SUCCESSFULLY")
        
    #     # -------------------------------
    #     # Step 2: Place THEORY (6-Day Version)
    #     # -------------------------------
    #     for subject, hours in theory:
    #         placed = 0
    #         # The while loop ensures we keep trying until all 'hours' are placed
    #         while placed < hours:
    #             starting_placed = placed
    #             for day in days:
    #                 if placed >= hours: 
    #                     break
                    
    #                 # Rule: Don't repeat the same subject on the same day order
    #                 if subject in timetable[day].values():
    #                     continue

    #                 for p in range(1, max_periods + 1):
    #                     if timetable[day][p] is None:
    #                         timetable[day][p] = subject
    #                         placed += 1
    #                         break
                
    #             # Safety: If a full cycle through 6 days placed nothing, stop to avoid infinite loop
    #             if placed == starting_placed:
    #                 break


    #     print("STEP2 SUCCESSFULLY")
        
    #     # -------------------------------
    #     # Step 3: Save to DB
    #     # -------------------------------
    #     for day in days:
    #         for period in range(1, max_periods + 1):
    #             cell = timetable[day][period]
    #             if cell:
    #                 sub_id = cell[0]

    #                 staff = query_db("""
    #                     SELECT staff_id 
    #                     FROM staff_subject_map 
    #                     WHERE subject_id=? 
    #                     LIMIT 1
    #                 """, (sub_id,), one=True)

    #                 staff_id = staff[0] if staff else None

    #                 query_db("""
    #                     INSERT INTO timetable
    #                     (department, semester, day, period, subject_id, staff_id)
    #                     VALUES (?, ?, ?, ?, ?, ?)
    #                 """, (department, semester, day, period, sub_id, staff_id))

    #     print("tIMETABLE GENERATED SUCCESSFULLY")
        
    #     return redirect("/student")

    @app.route("/generate/<int:semester>/<string:department>")
    def generate_timetable(semester, department):
        print("generate_timetable - ENTRY")
        days = ["Day-1", "Day-2", "Day-3", "Day-4", "Day-5"]
        max_periods = 5

          # --- PRE-REQUISITE CHECK ---
        # 1. Check if any subjects exist
        subjects_count = query_db("""
            SELECT COUNT(*) as count FROM subjects 
            WHERE semester=? AND department=?
        """, (semester, department), one=True)

        if not subjects_count or subjects_count['count'] == 0:
            return jsonify({"success": False, "message": "No subjects found for this Semester/Department. Please add subjects first."}), 400

        # 2. Check if total hours exceed availability (5 days * 5 periods = 25)
        total_hours = query_db("""
            SELECT SUM(hours_per_week) as total FROM subjects 
            WHERE semester=? AND department=?
        """, (semester, department), one=True)
        
        if total_hours['total'] and total_hours['total'] > 25:
            return jsonify({"success": False, "message": f"Total hours ({total_hours['total']}) exceed weekly capacity (25)."}), 400

        # 3. Check if any subjects are missing staff assignments
        unassigned = query_db("""
            SELECT s.subject_name FROM subjects s
            LEFT JOIN staff_subject_map m ON s.id = m.subject_id
            WHERE s.semester=? AND s.department=? AND m.staff_id IS NULL
        """, (semester, department))

        if unassigned:
            names = ", ".join([r['subject_name'] for r in unassigned])
            return jsonify({"success": False, "message": f"Missing staff for: {names}"}), 400


        # 1. Clear old timetable for this specific selection
        print("Clear old timetable - ENTRY")
        query_db(
            "DELETE FROM timetable WHERE department=? AND semester=?",
            (department, semester)
        )

        # 2. Fetch subjects
        # IMPORTANT: Ensure subject_id is the first column for easy indexing
        subjects = query_db("""
            SELECT id, subject_type, hours_per_week
            FROM subjects
            WHERE department=? AND semester=?
        """, (department, semester))

        # --- IF ALL PASS, PROCEED WITH GENERATION ---
        print("Pre-requisites met. Starting generation...")

        # Initialize empty timetable structure
        timetable = {
            day: {p: None for p in range(1, max_periods + 1)}
            for day in days
        }

        # 3. Separate labs and theory (FIX: Unpack sub_id explicitly)
        labs = []
        theory = []

        for sub_id, s_type, hours in subjects:
            if s_type and s_type.lower() == "lab":
                labs.append((sub_id, 2))  # Lab = 2 consecutive periods
            else:
                # Default to 0 hours if None to avoid type errors
                h = int(hours) if hours else 0
                theory.append((sub_id, h))

        print("PRIOR TO ALL STEPS - ENTRY")
        
        # -------------------------------
        # Step 1: Place LABS (Consecutive slots)
        # -------------------------------
        day_index = 0
        for lab_id, duration in labs:
            placed = False
            while not placed and day_index < len(days):
                day = days[day_index]
                for p in range(1, max_periods): # Look for p and p+1
                    if timetable[day][p] is None and timetable[day][p+1] is None:
                        timetable[day][p] = lab_id
                        timetable[day][p+1] = lab_id
                        placed = True
                        break
                day_index += 1

        print("STEP1 (LABS) SUCCESSFULLY")
        
        # -------------------------------
        # Step 2: Place THEORY
        # -------------------------------
        for sub_id, hours in theory:
            placed_count = 0
            # Keep trying until all required hours for this subject are filled
            while placed_count < hours:
                starting_placed = placed_count
                for day in days:
                    if placed_count >= hours: 
                        break
                    
                    # Rule: Don't repeat the same subject on the same day
                    if sub_id in timetable[day].values():
                        continue

                    for p in range(1, max_periods + 1):
                        if timetable[day][p] is None:
                            timetable[day][p] = sub_id
                            placed_count += 1
                            break
                
                # Safety: If a full cycle through all days placed nothing, break to avoid infinite loop
                if placed_count == starting_placed:
                    print(f"Warning: Could not place all hours for subject {sub_id}")
                    break

        print("STEP2 (THEORY) SUCCESSFULLY")

         # -------------------------------
        # Step 2.5: Fill Empty Slots (New)
        # -------------------------------
        # If any slot is still None, fill it with a placeholder to ensure 25 rows
        for day in days:
            for p in range(1, max_periods + 1):
                if timetable[day][p] is None:
                    # You can use a specific 'Library' ID or just 'Free'
                    timetable[day][p] = "Library" 

        print("ALL 25 SLOTS VERIFIED")
        
        # -------------------------------
        # Step 3: Save to DB
        # -------------------------------
        for day in days:
            for period in range(1, max_periods + 1):
                sub_id = timetable[day][period]
                
                # Check if it's a real subject or our placeholder
                if sub_id == "FREE_SLOT" or sub_id == "Library" or sub_id == "":
                    # Option A: Skip insert (results in < 25 rows)
                    # Option B: Insert with NULL subject_id (results in 25 rows)
                    query_db("""
                        INSERT INTO timetable (department, semester, day, period, subject_id, staff_id)
                        VALUES (?, ?, ?, ?, NULL, NULL)
                    """, (department, semester, day, period))
                    continue

                if sub_id:
                    staff = query_db("""
                        SELECT staff_id FROM staff_subject_map 
                        WHERE subject_id=? LIMIT 1
                    """, (sub_id,), one=True)
                    
                    staff_id = staff[0] if staff else None

                    query_db("""
                        INSERT INTO timetable (department, semester, day, period, subject_id, staff_id)
                        VALUES (?, ?, ?, ?, ?, ?)
                    """, (department, semester, day, period, sub_id, staff_id))
        
        print("TIMETABLE GENERATED SUCCESSFULLY")
            # DO NOT return "" or redirect. Return this instead:
        return jsonify({
            "success": True, 
           "message": "Timetable generated successfully for " + department + " Semester " + str(semester)
        })
