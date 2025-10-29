/*
  Warnings:

  - You are about to drop the column `status` on the `collar_statuses` table. All the data in the column will be lost.
  - Added the required column `prediction` to the `collar_statuses` table without a default value. This is not possible if the table is not empty.

*/
-- AlterTable
ALTER TABLE "collar_statuses" DROP COLUMN "status",
ADD COLUMN     "prediction" TEXT NOT NULL;
