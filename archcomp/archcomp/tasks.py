print("importing tasks.py ....")
import time
import os
import subprocess


def process_file(uuid):
    try:
        import django

        django.setup()

        from archcomp.models import UploadedFile

        uploaded_file_obj = UploadedFile.objects.get(uuid=uuid)

        subprocess.call(
            [
                "scp",
                "-r",
                "processing/validation/models.cfg",
                str(uploaded_file_obj.folderpath),
            ]
        )

        cfg_string = f'(include "models.cfg")\n(set-log "validation-log.csv")\n(set-report "validation-report.csv")\n(validate "{uploaded_file_obj.filename}")'

        filename_withoutext = uploaded_file_obj.filename.split(".")[0]
        with open(
            os.path.join(uploaded_file_obj.folderpath, f"{filename_withoutext}.cfg"),
            "w",
        ) as f:
            f.write(cfg_string)

        p = subprocess.check_output(
            [
                "bash",
                "./../../processing/validation/falstar.sh",
                str(f"{filename_withoutext}.cfg"),
            ],
            cwd=str(uploaded_file_obj.folderpath),
        )

        if "Exception" in str(p):
            raise Exception

        uploaded_file_obj.status = "success"
        uploaded_file_obj.save()

    except UploadedFile.DoesNotExist:
        pass
    except Exception:
        print("Falstar Errored out")
        uploaded_file_obj.status = "failed"
        uploaded_file_obj.save()
