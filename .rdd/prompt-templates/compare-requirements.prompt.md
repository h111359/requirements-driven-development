## Parameters:

[Product-Requirements-Specification-File] = `` // Path to the Product Requirements Specification file to compare against.   

## Role:

You are an expert software requirements analyst. Your task is to compare two sets of software requirements and identify any differences, inconsistencies, or missing elements between them. 

## Context:

RDD maintains a file with the requirements understood by the framework in `.rdd-instance/requirements.md`. 

## Tasks:

1. Review the provided requirements from [Product-Requirements-Specification-File] and `.rdd-instance/requirements.md` carefully.
2. In `.rdd-instance/workdir` create or update a file (replace the content) named `compare-requirements.md` where you will document your comparison findings.
3. Identify and list any discrepancies, missing elements, or inconsistencies between the two sets of requirements.
4. Provide a full report of the differences and areas that may need clarification or further development in `.rdd-instance/workdir/compare-requirements.md`. Include sections for:
   - Missing Requirements in `.rdd-instance/requirements.md` document - generate new requirements to be added in the format used in `.rdd-instance/requirements.md`
   - Inconsistent Requirements between the two documents and sugestion which `.rdd-instance/requirements.md` to be updated (and how) to resolve them
   - Requirements in `.rdd-instance/requirements.md` which are invalid and should be removed or revised 