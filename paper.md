---
title: 'EspressoDB: A scientific database for managing high-performance computing workflows'
tags:
  - Python
  - Django
  - High-performance computing
  - Lattice QCD
authors:
  - name: Chia Cheng Chang
    orcid: 0000-0002-3790-309X
    affiliation: "1, 2, 3"
  - name: Christopher Körber
    orcid: 0000-0002-9271-8022
    affiliation: "2, 3"
  - name: André&#160;Walker-Loud
    orcid: 0000-0002-4686-3667
    affiliation: "3, 2"
affiliations:
 - name: iTHEMS RIKEN, Wako, Saitama 351-0198
   index: 1
 - name: Department of Physics, University of California, Berkeley, California 94720
   index: 2
 - name: Nuclear Science Division, Lawrence Berkeley National Laboratory, Berkeley, California 94720
   index: 3

date: 3 December 2019
bibliography: paper.bib

---

# Summary

Leadership computing facilities around the world support cutting-edge scientific research across a broad spectrum of disciplines including understanding climate change [@Kurth_2018], combating opioid addiction [@Joubert:2018:AOE:3291656.3291732], or simulating the decay of a neutron [@8665785].
While the increase in computational power has allowed scientists to better evaluate the
underlying model, the size of these computational projects has grown to a point where
a framework is desired to facilitate managing the workflow.
A typical scientific computing workflow includes:

1. Defining all input parameters for every step of the computation;
2. Defining dependencies of computational tasks;
3. Storing some of the output data;
4. Post-processing these data files;
5. Performing data analysis on output.


[EspressoDB](https://github.com/callat-qcd/espressodb/) is a programmatic object-relational mapping (ORM) data management framework implemented in Python and based on the [Django web framework](https://www.djangoproject.com).
EspressoDB was developed to streamline data management, centralize and promote data integrity, while providing domain flexibility and ease of use.
It is designed to directly integrate in utilized software to allow dynamical access to vast amount of relational data at runtime.
Compared to existing ORM frameworks like [SQLAlchemy](https://www.sqlalchemy.org) or Django itself, EspressoDB lowers the barrier of access by simplifying the project setup and provides further features to satisfy uniqueness and consistency over multiple data dependencies.
In contrast to software like [DVC](https://github.com/iterative/dvc),
[VisTrails](https://www.vistrails.org/index.php/Main_Page), or [Taverna](https://taverna.incubator.apache.org) [@10.1093/nar/gkt328], which describe the workflow of computations, EspressoDB rather interacts with data itself and thus can be used in a complementary spirit.

The framework provided by EspressoDB aims to support the ever-increasing complexity of workflows of scientific computing at leadership computing facilities (LCFs), with the goal of reducing the amount of human time required to manage the jobs, thus giving scientists more time to focus on science.

# Features
Data integrity is important to scientific projects and becomes more challenging the larger the project.
In general, a SQL framework type-checks data before writing to the database and controls dependencies and relations between different tables to ensure internal consistency.
EspressoDB allows additional user-defined constraints not supported by SQL (*e.g.* unique constraints using information across related tables).
Once the user has specified a set of conditions that entries have to fulfill for each table, EspressoDB runs these cross-checks for new data before inserting them in the database.

EspressoDB also supports collaborative and open-data oriented projects by leveraging and extending Django's ORM interface and web hosting component.
The object oriented approach allows the whole team to determine table architectures without knowing SQL.
Once tables have been implemented by users familiar with the details of the EspressoDB project, additional users can access data without detailed knowledge of the project itself.
In addition to providing a centralized data platform, it is possible to spawn customized web pages which can be hosted locally or on the world wide web[^1].
EspressoDB simplifies creating projects by providing default Django configurations that set up, for example, connections to the database and webpages to view associated tables.
For example, with the default setting, EspressoDB spawns:

* Documentation views of implemented tables;
* A project-wide notification system;
* Project-specific Python interface guidelines which help writing scripts to populate the database;
* Admin pages for interacting with data in a GUI.

Further views can be implemented to interact with data and use existing Python libraries for summarizing and visualizing information.
This allows users to create visual progress updates on the fly and to integrate the database information to the data-processing workflow, significantly reducing the human overhead required due to improved automation.

More details, usage instructions, and examples are documented at [espressodb.readthedocs.io](https://espressodb.readthedocs.io).

[^1]: Depending on the configuration, it is possible to provide selected access for multiple users on different levels.


# Use case
[LatteDB](https://github.com/callat-qcd/lattedb/), an application of EspressoDB, contains table definitions for lattice quantum chromodynamics (LQCD) calculations and analysis.
LatteDB is currently being used by the [CalLat Collaboration](https://a51.lbl.gov/~callat/webhome/) in their computations on Summit at the Oak Ridge Leadership Computing Facility ([OLCF](https://www.olcf.ornl.gov)) through DOE INCITE Allocations [@incite:2019; @incite:2020].
The website generated by LatteDB used by CalLat can be found at [https://ithems.lbl.gov/lattedb/](https://ithems.lbl.gov/lattedb/). A precursor to EspressoDB and LatteDB was used to support a series of LQCD projects [@Nicholson:2018mwc; @Chang:2018uxx].

Summit at OLCF is disruptively fast compared to previous generations of leadership-class computers.  There are two challenges which are both critical to address for near-exascale computers such as Summit, which will become more important in the exascale era:

1. _Efficient bundling and management of independent tasks_.
2. _Dependent task generation and data processing_;

Using lattice QCD as a specific example, the computations can be organized as a directed multigraph:
a single calculation requires tens-of-thousands to millions of independent MPI tasks to be completed. These tasks, while running independently, have nested and chained interdependencies (the output of some tasks are part of the input for other tasks).
Several such complete computations must be performed to extract final answers.
As a specific example, CalLat creates petabytes of temporary files that are written to the scratch file system, used for subsequent computations and ultimately processed down to hundreds of terabytes that are saved for analysis.
It is essential to track the status of these files in real-time to identify corrupt, missing, or purgeable files.

Understandably, LCFs prohibit the submission of millions of small tasks to their supercomputers (clogged queues, overtaxed service nodes, etc.).
It is therefore imperative to have a task manager capable of bundling many tasks into large jobs while distributing the work to various components of the heterogeneous nodes;
To keep the nodes from going idle, the jobs must be backfilled while running with the next set of available tasks (item 1).
Members of CalLat are addressing the task bundling through the creation of job management software, [METAQ](https://github.com/evanberkowitz/metaq) [@Berkowitz:2017vcp], and ``MPI_JM`` [@8665785; @Berkowitz:2017xna], while
LatteDB is designed to address the dependent task generation.
A future feature of LatteDB  is integration with ``MPI_JM``.

For the second item, keeping track of the tasks, optimizing the order of tasks and ensuring no work is repeated requires a task manager that understands all these dependencies and the uniqueness of each task.  Software to track and manage such a computational model at runtime, which does not require in-depth knowledge of, e.g., managing databases, does not currently exist, which motivated the creation of EspressoDB and LatteDB.





# Acknowledgements

We thank Evan Berkowitz, Arjun Gambhir, Ben Hörz,  Kenneth McElvain and Enrico Rinaldi for useful insights and discussions which helped in creating EspressoDB and LatteDB.
C.K. gratefully acknowledges funding through the Alexander von Humboldt Foundation through a Feodor Lynen Research Fellowship.
The work of A.W-L. was supported by the Exascale Computing Project (17-SC-20-SC), a joint project of the U.S. Department of Energy's Office of Science and National Nuclear Security Administration, responsible for delivering a capable exascale ecosystem, including software, applications, and hardware technology, to support the nation's exascale computing imperative.

This research used resources of the Oak Ridge Leadership Computing Facility, which is a DOE Office of Science User Facility supported under Contract DE-AC05-00OR22725, with access and computer time granted through the DOE INCITE Program.

# References
